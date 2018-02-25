#include<iostream>
#include "ros/ros.h"

#include "std_msgs/Empty.h"
#include "std_msgs/String.h"
#include "std_msgs/Float64.h"
#include "ardrone_autonomy/Navdata.h"
#include "geometry_msgs/Twist.h"

using namespace std;

float dev = 0;
int flag = 0;

void stair_climb(const std_msgs::Float64::ConstPtr& data){
    dev = data->data;

}


int main(int argc, char** argv){
    ros::init(argc, argv, "climb_stairs");
    ros::NodeHandle n;
    ros::Rate loop_rate(10);
    geometry_msgs::Twist command;
    double time_start = ros::Time::now().toSec();
    double seconds = 0.0, time_now = 0.0, land_time = 0 ;

    ros::Subscriber dev_sub = n.subscribe("ardrone/str_dev", 1, stair_climb);

    ros::Publisher pub_takeOff = n.advertise<std_msgs::Empty>("ardrone/takeoff", 1000);
    ros::Publisher pub_land = n.advertise<std_msgs::Empty>("ardrone/land", 1000);
    ros::Publisher pub_reset = n.advertise<std_msgs::Empty>("ardrone/reset", 1000);
    ros::Publisher pub_command = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);

    while (ros::ok()){
        
        while(seconds<4 && flag == 0){
            time_now = ros::Time::now().toSec();
            seconds = time_now - time_start;
            cout << seconds << "Taking Off"<<endl;
            pub_takeOff.publish(std_msgs::Empty());
        }
        flag = 1;
        seconds = 0;
        land_time = ros::Time::now().toSec() - time_start;
        
        while(flag == 1 && land_time > 50 && land_time < 55){
            //time_now = ros::Time::now().toSec();
            //seconds = time_now - time_start;
            cout<< land_time;
            cout << "Landing"<<endl;
            pub_land.publish(std_msgs::Empty());
        }




        if (dev < -10){
            command.linear.x = 0;
            command.linear.y = 0;
            command.linear.z = 0;
            command.angular.z = -0.3;   // Turning Right
            pub_command.publish(command);
        }

        else if (dev > 10){
            command.linear.x = 0;
            command.linear.y = 0;
            command.linear.z = 0;
            command.angular.z = 0.3;    // Turning Left
            pub_command.publish(command);
        }

        else {
            command.linear.x = 0.2;
            command.linear.y = 0;
            command.linear.z = 0;
            command.angular.z = 0;
            pub_command.publish(command);
        }

        loop_rate.sleep();

    }
    ros::spin();
    return 0;
}