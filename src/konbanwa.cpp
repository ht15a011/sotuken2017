#include <ros/ros.h>

int main(int argc, char **argv)
{
	ros::init(argc, argv, "KONBANWA");
	ros::NodeHandle nh;
	
	ros::Rate rate(1);
	while(ros::ok()){
		ROS_INFO_STREAM("KONBANWA !");
		rate.sleep();
	}
	
	return 0;
}
