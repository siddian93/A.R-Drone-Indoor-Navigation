import rospy
import numpy as np
from time import time

from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata


rot_x, rot_y, rot_z = [], [], []
v_x, v_y, v_z = [], [], []
a_x, a_y, a_z = [], [], []
battery = []
def get_Navdata(data):
    t = int(time())
    if t%5 == 0:
        print 'Dude'
        rot_x.append(data.rotX)
        rot_y.append(data.rotY)
        rot_z.append(data.rotZ)
        v_x.append(data.vx)
        v_y.append(data.vy)
        v_y.append(data.vy)
        a_x.append(data.ax)
        a_y.append(data.ay)
        a_z.append(data.az)
        battery.append(data.batteryPercent)
        rotx = np.asarray(rot_x)
        roty = np.asarray(rot_y)
        rotz = np.asarray(rot_z)
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/rotx.csv', rotx, delimiter=',')
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/roty.csv', roty, delimiter=',')
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/rotz.csv', rotz, delimiter=',')
        vX = np.asarray(v_x)
        vY = np.asarray(v_y)
        vZ = np.asarray(v_z)
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/vX.csv', vX, delimiter=',')
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/vY.csv', vY, delimiter=',')
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/vZ.csv', vZ, delimiter=',')
        aX = np.asarray(a_x)
        aY = np.asarray(a_y)
        aZ = np.asarray(a_z)
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/aX.csv', aX, delimiter=',')
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/aY.csv', aY, delimiter=',')
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/aZ.csv', aZ, delimiter=',')
        bat = np.asarray(battery)
        np.savetxt('/home/siddhartha/ros_ws/src/saxena_drone/scripts/bat.csv', bat, delimiter=',')
        print data.batteryPercent
        #rospy.sleep(3)
        #rospy.signal_shutdown('Landing and Shutting Down')

def navdata_handle():
    rospy.init_node("ND")
    while True :
        #print 'Hello'
        nav_sub = rospy.Subscriber('/ardrone/navdata', Navdata, get_Navdata)
        rospy.sleep(1)
        nav_sub = None
        rospy.sleep(1)
        print 'Dude1'

    #print val
    #rospy.sleep()
    
