#include <string>
#include <ros/ros.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <vector>

int main(int argc, char **argv) {
	ros::init(argc, argv, "suriasi_publisher");
	ros::NodeHandle nh;
	ros::Publisher joint_pub = nh.advertise<trajectory_msgs::JointTrajectory>("/KHR_3HV/torque_control/set_joint_trajectory", 10);
	
	ros::Rate loop_rate(10);
	
	const double radHips = 30 * (M_PI/180);
	const double radone = 1 * (M_PI/180);
	const int size = 6;
	
	
	while(ros::ok()){
	trajectory_msgs::JointTrajectory joint_state;
	joint_state.joint_names.resize(size);
	joint_state.points.resize(size);
	
	joint_state.header.stamp = ros::Time::now();
	
	joint_state.joint_names[0] ="body_2_to_Lhips";
    joint_state.joint_names[1] ="body_2_to_Rhips";
    joint_state.joint_names[2] ="Lshin_to_Lankle";
    joint_state.joint_names[3] ="Rshin_to_Rankle";
    joint_state.joint_names[4] ="Lankel_to_Lfoot";
    joint_state.joint_names[5] ="Rankel_to_Rfoot";
    
    joint_state.points.resize(1);
    
    int p = 0;
    joint_state.points[p].positions.resize(size);
    joint_state.points[p].positions[0] = -1 * radHips;
	joint_state.points[p].positions[1] = radHips ;
	joint_state.points[p].positions[2] = radone;
	joint_state.points[p].positions[3] = -1 * radone;
	joint_state.points[p].positions[4] = radone;
	joint_state.points[p].positions[5] = -1 * radone;

	joint_state.points[p].time_from_start = ros::Duration(1.0);
	joint_pub.publish(joint_state);
	
	loop_rate.sleep();
	ros::spinOnce();
	}

	return 0;
/*	
	joint_state.points[p].positions[0].time_from_start = ros::Duration(1.0);
	joint_state.points[p].positions[1].time_from_start = ros::Duration(1.0);
	joint_state.points[p].positions[2].time_from_start = ros::Duration(0.0);
	joint_state.points[p].positions[3].time_from_start = ros::Duration(0.0);
	joint_state.points[p].positions[4].time_from_start = ros::Duration(0.0);
	joint_state.points[p].positions[5].time_from_start = ros::Duration(0.0);
	
	

	r.sleep();
	ros::spinOnce();
	
	
	const int loop = 2;
	while(ros::ok()){
		for(int i=0;i<loop;i++){
			joint_state.header.stamp = ros::Time::now();
			std::vector<trajectory_msgs::JointTrajectoryPoint> points(6);
			
		}
		
	}
	*/
}
