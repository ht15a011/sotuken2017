#!/usr/bin/env python
# coding: utf-8

import sys
import os
import math
import rospy 
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

#
# Functions.
# 並行摺足の動作を1回行う関数

def publish_khr_3hv_jointtrajectory(khrdeg = 0):
    oneDeg_rad = math.radians(1)		# 1度のラジアンを計算して，変数に格納
    rad = math.radians(khrdeg)			# 関節を曲げる角度をラジアンに変更
    pub = rospy.Publisher('/KHR_3HV/torque_control/set_joint_trajectory', JointTrajectory, latch=True, queue_size=10)
    rospy.init_node('khr_3hv__choreonoid_ros', anonymous=True)
    msg = JointTrajectory()
    
    Lhips = 'body_2_to_Lhips'
    Rhips = 'body_2_to_Rhips'
	
    msg.joint_names = [ Lhips ]
    msg.points = []
    p = JointTrajectoryPoint()
    p.time_from_start = rospy.rostime.Duration(0)
    
    bend = 0.0
    while bend == khrdeg:
		if khrdeg < 0:
			p.positions = [ bend ]
			bend -= oneDeg_rad
		else:
			p.positions = [ bend ]
			bend += oneDeg_rad
		msg.points.append(p)
		rospy.loginfo(msg)
		pub.publish(msg)
		r = rospy.Rate(10)
		r.sleep()

def usage():
    name = os.path.basename(sys.argv[0])
    
    print 'error: invalid parameter'
    print ''
    print 'Set joint angle for KHR-3HV robot.'
    print 'usage: ' + name + ' [joint angle (degree)]'
    print '[joint angle] setting is range from -30.0 to 30.0.'
    
    return

# 
# Main.  
#

if __name__ == '__main__':
    is_error = True

    try:
        if len(sys.argv) == 2:
            jointDeg = float(sys.argv[1])  # set joint degree

            if (-30.0 <= jointDeg and jointDeg <= 30.0):
                publish_khr_3hv_jointtrajectory(khrdeg = jointDeg)
                is_error = False
    except ValueError:
        pass
    except rospy.ROSInterruptException:
        pass

    if (is_error):
        usage()
        sys.exit(1)

    sys.exit(0)
