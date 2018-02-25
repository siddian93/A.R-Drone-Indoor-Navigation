#include<iostream>
#include "ros/ros.h"

#include "std_msgs/Empty.h"
#include "std_msgs/String.h"
#include "std_msgs/Float64.h"
#include "ardrone_autonomy/Navdata.h"
#include "geometry_msgs/Twist.h"

using namespace std;
/*
struct State{
    int stat=0;
}*st;
*/
int angle = 0, dist = 0;

/*
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

*/

void dist_callback(const std_msgs::Float64::ConstPtr& data){
    dist = data->data;

}

void angle_callback(const std_msgs::Float64::ConstPtr& data){
    angle = data->data;
}


int main(int argc, char** argv){
    ros::init(argc, argv, "hoover");
    ros::NodeHandle n;
    ros::Rate loop_rate(10);
    geometry_msgs::Twist command;
    double time_start = ros::Time::now().toSec();
    double seconds = 0.0, time_now = 0.0 ;
    int flag = 0;
    //ros::Subscriber sub = n.subscribe("ardrone/navdata", 10, nav_callback);
    ros::Subscriber sub_len = n.subscribe("ardrone/template_dist", 1, dist_callback);
    ros::Subscriber sub_angle = n.subscribe("ardrone/template_angle", 1, angle_callback);
    ros::Publisher pub_takeOff = n.advertise<std_msgs::Empty>("ardrone/takeoff", 1000);
    ros::Publisher pub_land = n.advertise<std_msgs::Empty>("ardrone/land", 1000);
    ros::Publisher pub_reset = n.advertise<std_msgs::Empty>("ardrone/reset", 1000);
    ros::Publisher pub_command = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
    //ROS_INFO("Getting Battery Percent :....");

    while(ros::ok()){
        //cout << "Angle: "<<angle<<endl;
        //cout << "Dist: "<<dist<<endl;
        
        while(seconds<4 && flag == 0){
            time_now = ros::Time::now().toSec();
            seconds = time_now - time_start;
            //cout << seconds << "Taking Off"<<endl;
            pub_takeOff.publish(std_msgs::Empty());
        }
        flag = 1;
        seconds = 0;
        time_now =  ros::Time::now().toSec();

        if (dist> 20){
            cout<<angle<<endl;
            if (angle > 270 || angle < 90){
                command.linear.x = 0;
                command.linear.y = 0;
                command.linear.z = 0;
                command.angular.z = -0.3;
                pub_command.publish(command);
                cout<< "Turning Right"<<endl;
            }

            else if (angle < 270 || angle > 90){
                command.linear.x = 0;
                command.linear.y = 0;
                command.linear.z = 0;
                command.angular.z = 0.5;
                pub_command.publish(command);
                cout<< "Turning Left" << endl;
            }
        }

        else{
            command.linear.x = 0;
            command.linear.y = 0;
            command.linear.z = 0;
            command.angular.z = 0;
            pub_command.publish(command);
            cout<<"Hoovering" << endl;

        }
        /*
        while (dist != 0){
            if (angle > 270 && angle < 90){
                command.linear.x = 0;
                command.linear.y = 0;
                command.linear.z = 0.5;
                command.angular.z = 0;
                pub_command.publish(command);
                time_now = ros::Time::now().toSec();
                if (time_now - time_start > 40){
                    cout<<"breaking 1"<< endl;
                    break;
                }
            }

            if (angle < 270 && angle > 90){
                command.linear.x = 0;
                command.linear.y = 0;
                command.linear.z = -0.5;
                command.angular.z = 0;
                pub_command.publish(command);
                time_now = ros::Time::now().toSec();
                if (time_now - time_start > 40){
                    cout<<"breaking 2"<< endl;
                    break;
                }
            }
            
        }
        */
        seconds = 0;
        time_now =  ros::Time::now().toSec();
        if (time_now - time_start >40){
            double time_land = ros::Time::now().toSec();
            while (seconds<4 && flag == 1){
                time_now = ros::Time::now().toSec();
                seconds= time_now - time_land;
                //cout<< seconds << "Landing"<<endl;
                pub_land.publish(std_msgs::Empty());
            }

        } 
        flag = 2;
        
        
        ros::spinOnce();
        loop_rate.sleep();
        //ros::shutdown();
    }

    /*
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
            while(seconds<30){
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
    */
    ros::spin();
    return 0;
}