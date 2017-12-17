#include <string>
#include <ros/ros.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <vector>

int main(int argc, char **argv) {
	ros::init(argc, argv, "suriasi_publisher");
	ros::NodeHandle nh;
	ros::Publisher joint_pub = nh.advertise<trajectory_msgs::JointTrajectory>("/KHR_3HV/torque_control/set_joint_trajectory", 10);
		
	const int rate = 100;
	const int size = 6;
	const int phase = 4;
	
	const double radHips = 30 * (M_PI/180);
	const double radone = 1 * (M_PI/180);

	trajectory_msgs::JointTrajectory joint_state;
	joint_state.joint_names.resize(size);
	joint_state.points.resize(phase);
	
	joint_state.joint_names[0] ="body_2_to_Lhips";
	joint_state.joint_names[1] ="body_2_to_Rhips";
	joint_state.joint_names[2] ="Lshin_to_Lankle";
	joint_state.joint_names[3] ="Rshin_to_Rankle";
	joint_state.joint_names[4] ="Lankel_to_Lfoot";
	joint_state.joint_names[5] ="Rankel_to_Rfoot";
	
	ros::Rate r(rate);
	for(int i=0;i<10;i++){
	joint_state.header.stamp = ros::Time::now() + ros::Duration(1.0);
	
	int p = 0;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = 0.0;
	joint_state.points[p].positions[1] = 0.0;
	joint_state.points[p].positions[2] = radone;
	joint_state.points[p].positions[3] = radone;
	joint_state.points[p].positions[4] = -1 * radone;
	joint_state.points[p].positions[5] = radone;

	joint_state.points[p].time_from_start = ros::Duration(0);
	
	p = 1;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = radHips;
	joint_state.points[p].positions[1] = radHips;
	joint_state.points[p].positions[2] = 0.0;
	joint_state.points[p].positions[3] = 0.0;
	joint_state.points[p].positions[4] = 0.0;
	joint_state.points[p].positions[5] = 0.0;

	joint_state.points[p].time_from_start = ros::Duration(2.0);
	
	p = 2;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = 0.0;
	joint_state.points[p].positions[1] = 0.0;
	joint_state.points[p].positions[2] = -1 * radone;
	joint_state.points[p].positions[3] = -1 * radone;
	joint_state.points[p].positions[4] = -1 * radone;
	joint_state.points[p].positions[5] = radone;

	joint_state.points[p].time_from_start = ros::Duration(5.0);
		
	p = 3;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = -1 * radHips;
	joint_state.points[p].positions[1] = -1 * radHips;
	joint_state.points[p].positions[2] = 0.0;
	joint_state.points[p].positions[3] = 0.0;
	joint_state.points[p].positions[4] = 0.0;
	joint_state.points[p].positions[5] = 0.0;
	
	joint_state.points[p].time_from_start = ros::Duration(7.0);
	
	for(int i=0;i<rate;i++){
		joint_pub.publish(joint_state);
		r.sleep();
	}
}
	return 0;
}
