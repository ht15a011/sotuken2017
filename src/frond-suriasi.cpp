#include <string>
#include <ros/ros.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <vector>

int main(int argc, char **argv) {
	ros::init(argc, argv, "suriasi_publisher");
	ros::NodeHandle nh;
	ros::Publisher joint_pub = nh.advertise<trajectory_msgs::JointTrajectory>("/KHR_3HV/torque_control/set_joint_trajectory", 10);
		
	const int rate = 100;
	const int size = 8;
	const int phase = 4;
	
	const double rad5 = 5 * (M_PI/180);
	const double rad20 = 20 * (M_PI/180);

	trajectory_msgs::JointTrajectory joint_state;
	joint_state.joint_names.resize(size);
	joint_state.points.resize(phase);
	
	joint_state.joint_names[0] ="Lhips_to_Lthigh";
	joint_state.joint_names[1] ="Rhips_to_Rthigh";
	joint_state.joint_names[2] ="Lthigh_to_Lknee";
	joint_state.joint_names[3] ="Rthigh_to_Rknee";
	joint_state.joint_names[4] ="Lshin_to_Lankle";
	joint_state.joint_names[5] ="Rshin_to_Rankle";
	joint_state.joint_names[6] ="Lankle_to_Lfoot";
	joint_state.joint_names[7] ="Rankle_to_Rfoot";
	
	ros::Rate r(rate);
	joint_state.header.stamp = ros::Time::now() + ros::Duration(1.0);
	
	int p = 0;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = -1 * rad5;
	joint_state.points[p].positions[1] = -1 * rad5;
	joint_state.points[p].positions[2] = 0.0;
	joint_state.points[p].positions[3] = 0.0;
	joint_state.points[p].positions[4] = 0.0;
	joint_state.points[p].positions[5] = 0.0;
	joint_state.points[p].positions[6] = rad5;
	joint_state.points[p].positions[7] = rad5;

	joint_state.points[p].time_from_start = ros::Duration(0);
	
	p = 1;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = -1 * rad5;
	joint_state.points[p].positions[1] = -1 * rad5;
	joint_state.points[p].positions[2] = 0.0;
	joint_state.points[p].positions[3] = -1 * rad20;
	joint_state.points[p].positions[4] = 0.0;
	joint_state.points[p].positions[5] = 0.0;
	joint_state.points[p].positions[6] = rad5;
	joint_state.points[p].positions[7] = rad5;

	joint_state.points[p].time_from_start = ros::Duration(2.0);

	p = 2;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = rad5;
	joint_state.points[p].positions[1] = rad5;
	joint_state.points[p].positions[2] = rad20;
	joint_state.points[p].positions[3] = 0.0;
	joint_state.points[p].positions[4] = -1 * rad20;
	joint_state.points[p].positions[5] = 0.0;
	joint_state.points[p].positions[6] = -1 * rad5;
	joint_state.points[p].positions[7] = -1 * rad5;
	
	joint_state.points[p].time_from_start = ros::Duration(5.0);
		
	p = 3;
	joint_state.points[p].positions.resize(size);
	joint_state.points[p].positions[0] = rad5;
	joint_state.points[p].positions[1] = rad5;
	joint_state.points[p].positions[2] = -1 * rad20;
	joint_state.points[p].positions[3] = 0.0;
	joint_state.points[p].positions[4] = rad20;
	joint_state.points[p].positions[5] = 0.0;
	joint_state.points[p].positions[6] = -1 * rad5;
	joint_state.points[p].positions[7] = -1 * rad5;
	
	joint_state.points[p].time_from_start = ros::Duration(7.0);

	for(int i=0;i<10;i++){
		joint_pub.publish(joint_state);
		r.sleep();
	}
	return 0;
}
