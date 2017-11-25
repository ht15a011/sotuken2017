#!/usr/bin/env python

import roslib; roslib.load_manifest('walk_tools')
import rospy
import message_filters
import threading
import itertools

import numpy as np

from geometry_msgs.msg import Vector3Stamped, WrenchStamped

# Copied from camera_calibration.
class ApproximateSynchronizer(message_filters.SimpleFilter):
    def __init__(self, slop, fs, queue_size):
        message_filters.SimpleFilter.__init__(self)
        self.connectInput(fs)
        self.queue_size = queue_size
        self.lock = threading.Lock()
        self.slop = rospy.Duration.from_sec(slop)

    def connectInput(self, fs):
        self.queues = [{} for f in fs]
        self.input_connections = \
            [f.registerCallback(self.add, q) for (f, q) in zip(fs, self.queues)]

    def add(self, msg, my_queue):
        self.lock.acquire()
        my_queue[msg.header.stamp] = msg
        while len(my_queue) > self.queue_size:
            del my_queue[min(my_queue)]
        if 0:
            # common is the set of timestamps that occur in all queues
            common = reduce(set.intersection, [set(q) for q in self.queues])
            for t in sorted(common):
                # msgs is list of msgs (one from each queue) with stamp t
                msgs = [q[t] for q in self.queues]
                self.signalMessage(*msgs)
                for q in self.queues:
                    del q[t]
        else:
            for vv in itertools.product(*[q.keys() for q in self.queues]):
                if ((max(vv) - min(vv)) < self.slop):
                    msgs = [q[t] for q,t in zip(self.queues, vv)]
                    self.signalMessage(*msgs)
                    for q in self.queues:
                        try:
                            del q[t]
                        except KeyError:
                            pass # TODO: why can del q[t] fail?
        self.lock.release()

class ZmpEstimator(object):
    leftFootForceSensorTopic = None
    rightFootForceSensorTopic = None

    leftFootForceSensorSubscriber = None
    rightFootForceSensorSubscriber = None

    synchronizer = None
    synchronizerPrecision = 1e-3
    queueSize = 10

    timer = None

    zmpPublisher = None

    contactThreshold = 10

    leftFootPosition = [0., 0., 0.105]
    rightFootPosition = [0., 0., 0.105]
    referenceFrame = None

    startTime = rospy.Time(0)
    lastData = rospy.Time(0)

    def __init__(self):
        rospy.init_node('zmp_estimator')

        self.leftFootForceSensorTopic = \
            rospy.get_param('~left_foot_wrench', 'left_foot')
        self.rightFootForceSensorTopic = \
            rospy.get_param('~right_foot_wrench', 'right_foot')
        self.contactThreshold = \
            rospy.get_param('~contact_threshold',
                            ZmpEstimator.contactThreshold)
        self.synchronizerPrecision = \
            rospy.get_param('~approximate_sync',
                            ZmpEstimator.synchronizerPrecision)
        self.queueSize = \
            rospy.get_param('~queue_size', ZmpEstimator.queueSize)

        self.referenceFrame = \
            rospy.get_param('~reference_frame', '/world')
        self.leftFootPosition[0] = \
            rospy.get_param('~left_foot_x', ZmpEstimator.leftFootPosition[0])
        self.leftFootPosition[1] = \
            rospy.get_param('~left_foot_y', ZmpEstimator.leftFootPosition[1])
        self.leftFootPosition[2] = \
            rospy.get_param('~left_foot_z', ZmpEstimator.leftFootPosition[2])
        self.rightFootPosition[0] = \
            rospy.get_param('~right_foot_x', ZmpEstimator.rightFootPosition[0])
        self.rightFootPosition[1] = \
            rospy.get_param('~right_foot_y', ZmpEstimator.rightFootPosition[1])
        self.rightFootPosition[2] = \
            rospy.get_param('~right_foot_z', ZmpEstimator.rightFootPosition[2])

        self.leftFootForceSensorSubscriber = \
            message_filters.Subscriber(
            self.leftFootForceSensorTopic, WrenchStamped)
        self.rightFootForceSensorSubscriber = \
            message_filters.Subscriber(
            self.rightFootForceSensorTopic, WrenchStamped)

        self.synchronizer = \
            ApproximateSynchronizer(self.synchronizerPrecision,
                                    [self.leftFootForceSensorSubscriber,
                                     self.rightFootForceSensorSubscriber],
                                    self.queueSize)
        self.synchronizer.registerCallback(lambda l, r: self.callback (l, r))

        self.timer = rospy.Timer(rospy.Duration(1.),
                                 lambda x: self.callbackTimer(x))

        self.zmpPublisher = rospy.Publisher('zmp_estimated', Vector3Stamped)
        self.startTime = rospy.Time.now()

    def callback(self, leftFootForce, rightFootForce):
        if self.lastData == rospy.Time(0):
            rospy.loginfo(
                'synchronized forces received, starting.')
        self.lastData = leftFootForce.header.stamp

        rospy.logdebug('computing ZMP')
        zmp = Vector3Stamped()

        # Copy header (timestamp) from one of the two messages.
        # as they are almost equal, which one does not matter.
        zmp.header = leftFootForce.header

        # Fix frame id
        zmp.header.frame_id = ''

        # Compute ZMP from forces on feet.
        zmpLeftFoot = np.matrix([0., 0., 0.])
        zmpRightFoot = np.matrix([0., 0., 0.])

        leftFootOnFloor = False
        rightFootOnFloor = False

        if leftFootForce.wrench.force.z > self.contactThreshold:
            leftFootOnFloor = True
            zmpLeftFoot = np.matrix(
                [-leftFootForce.wrench.torque.y/leftFootForce.wrench.force.z,
                  leftFootForce.wrench.torque.x/leftFootForce.wrench.force.z,
                  0.])
            zmp.header.frame_id = leftFootForce.header.frame_id
        if rightFootForce.wrench.force.z > self.contactThreshold:
            rightFootOnFloor = True
            zmpRightFoot = np.matrix(
                [-rightFootForce.wrench.torque.y/rightFootForce.wrench.force.z,
                  rightFootForce.wrench.torque.x/rightFootForce.wrench.force.z,
                  0.])
            zmp.header.frame_id = rightFootForce.header.frame_id

        if not leftFootOnFloor and not rightFootOnFloor:
            zmp.vector.x = 0.
            zmp.vector.y = 0.
            zmp.vector.z = 0.
            zmp.header.frame_id = ''
        elif leftFootOnFloor and rightFootOnFloor:
            forceLeftFoot = np.matrix([leftFootForce.wrench.force.x,
                                       leftFootForce.wrench.force.y,
                                       leftFootForce.wrench.force.z])
            forceRightFoot = np.matrix([rightFootForce.wrench.force.x,
                                        rightFootForce.wrench.force.y,
                                        rightFootForce.wrench.force.z])

            momentLeftFoot = np.matrix([leftFootForce.wrench.torque.x,
                                        leftFootForce.wrench.torque.y,
                                        leftFootForce.wrench.torque.z])
            momentRightFoot = np.matrix([rightFootForce.wrench.torque.x,
                                         rightFootForce.wrench.torque.y,
                                         rightFootForce.wrench.torque.z])

            Mo = momentRightFoot \
                + np.cross(self.rightFootPosition, forceRightFoot) \
                + momentLeftFoot \
                + np.cross(self.leftFootPosition, forceLeftFoot)
            forces = forceLeftFoot + forceRightFoot

            zmp.vector.x = -Mo[0,1] / forces[0,2]
            zmp.vector.y = Mo[0,0] / forces[0,2]
            zmp.vector.z = 0.
            zmp.header.frame_id = self.referenceFrame
        elif leftFootOnFloor:
            zmp.vector.x = zmpLeftFoot[0]
            zmp.vector.y = zmpLeftFoot[1]
            zmp.vector.z = zmpLeftFoot[2]
        else:
            zmp.vector.x = zmpRightFoot[0]
            zmp.vector.y = zmpRightFoot[1]
            zmp.vector.z = zmpRightFoot[2]

        # In all cases, publish ZMP
        self.zmpPublisher.publish(zmp)

    def callbackTimer(self, x):
        if self.lastData == rospy.Time(0) and \
                rospy.Time.now() - self.startTime > rospy.Duration(2.):
            rospy.logwarn(
                'The node is not receiving any data.\n'
                + 'Please double check that your topics '
                + 'are sending synchronized data.')
            return
        if self.lastData == rospy.Time(0):
            return
        if rospy.Time.now() - self.lastData > rospy.Duration(1.):
            return

        rospy.logwarn(
            "last data reception was {0} second(s) ago".format(
                rospy.Time.now() - self.lastData))


    def spin(self):
        rospy.loginfo("waiting for {0} and {1} topics...".format(
                self.leftFootForceSensorTopic,
                self.rightFootForceSensorTopic))
        rospy.spin()

if __name__ == "__main__":
    estimator = ZmpEstimator()
    estimator.spin()
	