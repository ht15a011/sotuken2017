#include <string>
#include <ros/ros.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <vector>

class Robot_suriasi
{
	private:
		ros::NodeHandle nh;
		ros::Publisher joint_pub;
		trajectory_msgs::JointTrajectory joint_state;
		int size;
		int phase;
		double radHips;
		double radone;
		double time;
		int p;
		int count;
		int rate;
		
	public:
		Robot_suriasi()
		{
			joint_pub = nh.advertise<trajectory_msgs::JointTrajectory>("/KHR_3HV/torque_control/set_joint_trajectory", 10);
			
			size = 6;
			phase = 40;
			radHips = 5 * (M_PI/180);
			radone = 1 * (M_PI/180);
			time = 2;
			p = 0;
			count = 0;
			rate = 100;
			
			joint_state.joint_names.resize(size);
			joint_state.points.resize(phase);
			
			joint_state.joint_names[0] ="body_2_to_Lhips";
			joint_state.joint_names[1] ="body_2_to_Rhips";
			joint_state.joint_names[2] ="Lshin_to_Lankle";
			joint_state.joint_names[3] ="Rshin_to_Rankle";
			joint_state.joint_names[4] ="Lankel_to_Lfoot";
			joint_state.joint_names[5] ="Rankel_to_Rfoot";
		}
		
		~Robot_suriasi(){}
		
		void heikou_suriasi()
		{
			ros::Rate r(rate);
			while(count < 10){
			joint_state.header.stamp = ros::Time::now();
			
			joint_state.points[p].positions.resize(size);
			joint_state.points[p].positions[0] = 0.0;
			joint_state.points[p].positions[1] = 0.0;
			joint_state.points[p].positions[2] = radone;
			joint_state.points[p].positions[3] = radone;
			joint_state.points[p].positions[4] = radone;
			joint_state.points[p].positions[5] = -1 * radone;
			
			joint_state.points[p].time_from_start = ros::Duration(time);
	
			p += 1;
			time += 2;
			joint_state.points[p].positions.resize(size);
			joint_state.points[p].positions[0] = radHips;
			joint_state.points[p].positions[1] = radHips;
			joint_state.points[p].positions[2] = 0.0;
			joint_state.points[p].positions[3] = 0.0;
			joint_state.points[p].positions[4] = 0.0;
			joint_state.points[p].positions[5] = 0.0;

			joint_state.points[p].velocities.resize(size);
			for(size_t j = 0;j < size;j++){
				joint_state.points[p].velocities[j] = radHips;
			}
			joint_state.points[p].time_from_start = ros::Duration(time);
	
			p += 1;
			time += 5;
			joint_state.points[p].positions.resize(size);
			joint_state.points[p].positions[0] = 0.0;
			joint_state.points[p].positions[1] = 0.0;
			joint_state.points[p].positions[2] = -1 * radone;
			joint_state.points[p].positions[3] = -1 * radone;
			joint_state.points[p].positions[4] = radone;
			joint_state.points[p].positions[5] = -1 * radone;

			joint_state.points[p].time_from_start = ros::Duration(time);
		
			p += 1;
			time += 2;
			joint_state.points[p].positions.resize(size);
			joint_state.points[p].positions[0] = -1 * radHips;
			joint_state.points[p].positions[1] = -1 * radHips;
			joint_state.points[p].positions[2] = 0.0;
			joint_state.points[p].positions[3] = 0.0;
			joint_state.points[p].positions[4] = 0.0;
			joint_state.points[p].positions[5] = 0.0;
	
			joint_state.points[p].velocities.resize(size);
			for(size_t j = 0;j < size;j++){
				joint_state.points[p].velocities[j] = radHips;
			}
			
			joint_state.points[p].time_from_start = ros::Duration(time);
		}
			
			for(int i=0;i<10;i++){
				joint_pub.publish(joint_state);
				r.sleep();
			}
		}
};

int main(int argc, char **argv) {
	ros::init(argc, argv, "suriasi_publisher");
	
	Robot_suriasi motion;

	motion.heikou_suriasi();
	
	return 0;
}
