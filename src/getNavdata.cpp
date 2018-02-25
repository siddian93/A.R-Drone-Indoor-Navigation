#include<iostream>
#include "ros/ros.h"

#include "std_msgs/Empty.h"
#include "std_msgs/String.h"
#include "ardrone_autonomy/Navdata.h"
#include "geometry_msgs/Twist.h"

using namespace std;
/*
struct State{
    int stat=0;
}*st;
*/
int st;

void nav_callback(const ardrone_autonomy::Navdata::ConstPtr& data){
    //String s = data->batteryPercent;
    //int p = data->batteryPercent;
    //constant float p = data->batteryPercent;
    int bp = data->batteryPercent;
    int state = data->state;
    st = state;
    //st->stat = state;
    string s="";
    //ROS_INFO("Battery Percent : %d %%", bp);
    switch(state){
        case 1:
            s = "Initiated";
            break;
        case 2:
            s = "Landed";
            break;
        case 3:
        case 7:
            s = "Flying";
            break;
        case 4:
            s = "Hoovering";
            break;
        case 6:
            s = "Taking Off";
            break;
        case 8:
            s = "Landing";
            break;
        default :
            s = "Gathering Info";
    }
    ROS_INFO("Current State : %s", s.c_str());
    //cout<<s<<endl;

}


int main(int argc, char** argv){
    ros::init(argc, argv, "getNavdata");
    ros::NodeHandle n;
    ros::Rate loop_rate(1);
    geometry_msgs::Twist command;
    double time_start = ros::Time::now().toSec();
    double seconds = 0.0, time_now = 0.0 ;
    ros::Subscriber sub = n.subscribe("ardrone/navdata", 10, nav_callback);
    ros::Publisher pub_takeOff = n.advertise<std_msgs::Empty>("ardrone/takeoff", 1000);
    ros::Publisher pub_land = n.advertise<std_msgs::Empty>("ardrone/land", 1000);
    ros::Publisher pub_reset = n.advertise<std_msgs::Empty>("ardrone/reset", 1000);
    ros::Publisher pub_command = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
    ROS_INFO("Getting Battery Percent :....");
    
    while(ros::ok()){
        //cout << st << endl;
        //if(st == 2)
        seconds = 0;
        if (1){ //Takeoff
            while (seconds<4){
                time_now = ros::Time::now().toSec();
                seconds=time_now - time_start;
                //cout<< seconds;
                //ROS_INFO("Time : %f ", seconds);
                cout << seconds << "Taking Off"<<endl;
                pub_takeOff.publish(std_msgs::Empty());
            }
        }
        time_start = ros::Time::now().toSec();
        seconds = 0;
        if (1){ //Hoovering
            while(seconds<10){
                time_now = ros::Time::now().toSec();
                seconds=time_now - time_start;
                cout << seconds << "Hoovering"<<endl;
                command.linear.x = 0;
                command.linear.y = 0;
                command.linear.z = 0;
                command.angular.z = 0;
                pub_command.publish(command);
            }
        }
        
        time_start = ros::Time::now().toSec();
        seconds = 0;
        while(seconds < 10){
            time_now = ros::Time::now().toSec();
            seconds=time_now - time_start;
            cout << seconds << "Turning Left"<<endl;
            command.linear.x = 0;
            command.linear.y = 0;
            command.linear.z = 0;
            command.angular.z = 0.5;
            pub_command.publish(command);
        }

        time_start = ros::Time::now().toSec();
        seconds = 0;
        while(seconds < 10){
            time_now = ros::Time::now().toSec();
            seconds=time_now - time_start;
            cout << seconds << "Turning Right"<<endl;
            command.linear.x = 0;
            command.linear.y = 0;
            command.linear.z = 0;
            command.angular.z = -0.5;
            pub_command.publish(command);
        }





        time_start = ros::Time::now().toSec();
        seconds = 0;
        //if (st == 4)
        if (1){ // Landing
            while (seconds<4){
                time_now = ros::Time::now().toSec();
                seconds= time_now - time_start;
                cout<< seconds << "Landing"<<endl;
                pub_land.publish(std_msgs::Empty());
            }
        }
    
        ros::spinOnce();
        loop_rate.sleep();
        ros::shutdown();
        //break;
    }
    ros::spin();
    return 0;
}