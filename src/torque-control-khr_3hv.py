#!/usr/bin/env python
#
#

import sys
import os
import math
import rospy 
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

#
# Functions.
#

def publish_khr_3hv_jointtrajectory(khrname='base_link_to_head', khrdeg=0):
    rad = math.radians(khrdeg)
    pub = rospy.Publisher('/KHR_3HV/torque_control/set_joint_trajectory', JointTrajectory, latch=True, queue_size=10)
    rospy.init_node('khr_3hv__choreonoid_ros', anonymous=True)
    msg = JointTrajectory()
    msg.joint_names = [ khrname ]
    msg.points = []
    p = JointTrajectoryPoint()
    p.time_from_start = rospy.rostime.Duration(0)
    p.positions = [ rad ]

    msg.points.append(p)
    rospy.loginfo(msg)
    pub.publish(msg)
    rospy.Rate(1).sleep()

#
def check_khr_3hv_joint_name(khrname=''):
    names = { 
		'base_link': 0,					'Lthigh_to_Lknee': 0,
		'base_link_to_Lshoulder': 0,	'Lknee_to_Lshin': 0,
		'Lshoulder_to_Lupper_arm': 0,	'Lshin_to_Lankle': 0,
		'Lupper_arm_to_Llower_arm': 0,	'Lankle_to_Lfoot': 0,
		'base_link_to_Rshoulder': 0,	'body_2_to_Rhips': 0,
		'Rshoulder_to_Rupper_arm': 0,	'Rhips_to_Rthigh': 0,
		'Rupper_arm_to_Rlower_arm': 0,	'Rthigh_to_Rknee': 0,
		'base_link_to_body_2': 0,		'knee_to_Rshin': 0,
		'body_2_to_Lhips': 0,			'Rshin_to_Rankle': 0,
		'Lhips_to_Lthigh': 0,			'ankle_to_Rfoot': 0,
		'base_link_to_head': 0
        } 

    return khrname in names


#def usage():
#    name = os.path.basename(sys.argv[0])

#    print 'usage: ' + name + ' [joint name] [joint angle (degree)]'
#    print ''
#   print 'Set joint angle for JVRC-1 robot.'
#	print ''
#    print '[joint name] setting choose one of them:'
#	print '  base_link					Lthigh_to_Lknee'
#	print '  base_link_to_Lshoulder		Lknee_to_Lshin'
#	print '  Lshoulder_to_Lupper_arm	Lshin_to_Lankle'
#	print '  Lupper_arm_to_Llower_arm	Lankle_to_Lfoot'
#	print '  base_link_to_Rshoulder		body_2_to_Rhips'
#	print '  Rshoulder_to_Rupper_arm	Rhips_to_Rthigh'
#	print '  Rupper_arm_to_Rlower_arm	Rthigh_to_Rknee'
#	print '  base_link_to_body_2		knee_to_Rshin'
#	print '  body_2_to_Lhips			Rshin_to_Rankle'
#	print '  Lhips_to_Lthigh			ankle_to_Rfoot'
#	print '  base_link_to_head'
#    print ''
#   print '[joint angle] setting is range from 360.0 to -360.0.'
#    print ''
#    print 'e.g. if you want to change the joint angle of the base_link_to_head to degree of 40.'
#    print '  ' + name + ' base_link_to_head 40.0'
#    print ''

#    return

# 
# Main.  
#

if __name__ == '__main__':
    is_error = True

    try:
        if len(sys.argv) == 3:
            s = sys.argv[1]  #joint name
            f = float(sys.argv[2])  # set joint deg

            if (check_khr_3hv_joint_name(s) and (f <= 360.0 and f >= -360.0)):
                publish_khr_3hv_jointtrajectory(khrname=s, khrdeg=f)
                is_error = False
    except ValueError:
        pass
    except rospy.ROSInterruptException:
        pass

    if (is_error):
        #usage()
        sys.exit(1)

    sys.exit(0)
