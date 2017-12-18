#include <ros/ros.h>
#include <geometry_msgs/Wrench.h>

void Callback(const geometry_msgs::Wrench msg)
{
	float result[3];
	result[0] = msg.force.x;
	result[1] = msg.force.y;
	result[2] = msg.force.z;
	std::cout << "force.x: " << result[0] << std::endl;
	std::cout << "force.y: " << result[1] << std::endl;
	std::cout << "force.z: " << result[2] << std::endl;
}

int main(int argc, char **argv) {
	ros::init(argc, argv, "force_sensor_subscriber");
	
	ros::NodeHandle nh;
	
	ros::Subscriber force = nh.subscribe("/KHR_3HV/lfsensor1", 100, Callback);
	
	ros::spin();
	return 0;
}
