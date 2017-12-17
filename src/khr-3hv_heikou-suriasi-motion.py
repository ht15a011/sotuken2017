#!/usr/bin/env python
# coding: utf-8

import sys
import math
import rospy 
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

#
# Functions.
# 並行摺足を行う関数

def publish_khr_3hv_jointtrajectory():
	# ノードの名前を"khr_3hv_suriasi"にする
	rospy.init_node('khr_3hv_suriasi', anonymous=True)
	
	# 関節角度を指定して，摺足移動をするトピックを配信するPublisherの設定
	pub = rospy.Publisher('/KHR_3HV/torque_control/set_joint_trajectory', JointTrajectory, latch=True, queue_size=10)
    
	# 動かす関節のメッセージを初期化（hips,ankle,foot）
	msgLhips = JointTrajectory()
	msgRhips = JointTrajectory()
	msgLankle = JointTrajectory()
	msgRankle = JointTrajectory()
	msgLfoot = JointTrajectory()
	msgRfoot = JointTrajectory()
	
	msgLhips.joint_names = ['body_2_to_Lhips']
	msgLhips.points = []
	
	msgRhips.joint_names = [ 'body_2_to_Rhips' ]
	msgRhips.points = []
	
	msgLankle.joint_names = [ 'Lshin_to_Lankle' ]
	msgLankle.points = []
	
	msgRankle.joint_names = [ 'Rshin_to_Rankle' ]
	msgRankle.points = []
	
	msgLfoot.joint_names = [ 'Lankel_to_Lfoot' ]
	msgLfoot.points = []
	
	msgRfoot.joint_names = [ 'Rankel_to_Rfoot' ]
	msgRfoot.points = []
	
	# 関節角度の指令を出すメッセージの設定
	ponePlus = JointTrajectoryPoint()
	poneMinus = JointTrajectoryPoint()
	phipsPlus = JointTrajectoryPoint()
	phipsMinus = JointTrajectoryPoint()
	
	# 目標の関節角度までの時間を設定
	ponePlus.time_from_start = rospy.rostime.Duration(0.5)
	poneMinus.time_from_start = rospy.rostime.Duration(0.5)
	phipsPlus.time_from_start = rospy.rostime.Duration(1.0)
	phipsMinus.time_from_start = rospy.rostime.Duration(1.0)
    
    # 関節を曲げる角度をラジアンに変更
	hipsRad = math.radians(30)
	Degone = math.radians(1)
    
	rate = rospy.Rate(10)
	
	# Lankle と Lfoot の関節角度を設定
	ponePlus.positions = [ Degone ]
	msgLankle.points.append(ponePlus)
	msgLfoot.points.append(ponePlus)
	
	# Rankle と Rfoot の関節角度を設定
	poneMinus.positions = [ -Degone ]
	msgRankle.points.append(poneMinus)
	msgRfoot.points.append(poneMinus)
	
	# ankle と foot の関節角度を配信
	pub.publish(msgLankle)
	pub.publish(msgLfoot)
	pub.publish(msgRankle)
	pub.publish(msgRfoot)
	rate.sleep()
	
	rospy.sleep(1)
	
	# Lhips と Rhips の関節角度を設定
	phipsMinus.positions = [ -hipsRad ]
	msgLhips.points.append(phipsMinus)
		
	phipsPlus.positions = [ hipsRad ]
	msgRhips.points.append(phipsPlus)
	
	# Lhips と Rhips の関節角度を配信
	pub.publish(msgLhips)
	pub.publish(msgRhips)
		
	rate.sleep()

# 
# Main.  
#

if __name__ == '__main__':

    try:
		publish_khr_3hv_jointtrajectory()
    except rospy.ROSInterruptException: pass

    sys.exit(0)
