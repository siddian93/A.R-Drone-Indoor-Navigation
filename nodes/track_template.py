import rospy
import cv2
import time
import math
import numpy as np
from threading import Thread
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

time_start = int(time.time())

class store_template:
    temple = np.zeros((100, 100), dtype  = 'uint8')

bridge = CvBridge()
dist_pub = rospy.Publisher('/ardrone/template_dist', Float64, queue_size=1)
angle_pub = rospy.Publisher('/ardrone/template_angle', Float64, queue_size=1)
st = store_template()

def match():
    rospy.Rate(1)
    image_sub = rospy.Subscriber('/ardrone/image_rect_color', Image, callback)
    try :
        rospy.spin()
    except KeyboardInterrupt :
        print "Shutting Down"

def callback(data):
    dist, angle = 0, 0
    ang = Float64()
    d = Float64()
    w, h = 100, 100
    frame = bridge.imgmsg_to_cv2(data, "mono8")
    rgb = bridge.imgmsg_to_cv2(data, "bgr8")
    #print time.time()
    #if (int(time.time()) % 3 == 0) :
    if (int(time.time()) - time_start == 3):
    #if (True):
        #print time.time()
        template = frame[130:230, 270:370]
        st.temple = template
        #w, h = template.shape[: : -1]
        #print template.shape[: : -1]
    #print st.temple
    res = cv2.matchTemplate(frame, st.temple, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0]+w, top_left[1]+h)
    template_center = (top_left[0]+w/2, top_left[1]+h/2)
    dist = np.sqrt(np.square(template_center[0] - 320) + np.square(template_center[1] - 180))
    

    if (template_center[0] == 320 and template_center[1] == 180):
        angle = 0
        dist = 0
    
    elif (template_center[0] - 320 > 0 and template_center[1]-180 >0):
        angle = math.degrees(math.atan((template_center[1] - 180)/(template_center[0] - 320)))
        angle = 360 - angle
    
    elif (template_center[0]-320 <0 and template_center[1]-180 >0) :
        angle = math.degrees(math.atan((template_center[1] - 180)/(template_center[0] - 320)))
        angle = 180 - angle
    
    elif (template_center[0]-320 <0 and template_center[1]-180 <0) :
        angle = math.degrees(math.atan((template_center[1] - 180)/(template_center[0] - 320)))
        angle = 180 - angle
    
    elif (template_center[0]-320 >0 and template_center[1]-180 <0) :
        angle = math.degrees(math.atan((template_center[1] - 180)/(template_center[0] - 320)))
        angle = -angle
    
    elif (template_center[0]-320 == 0 and template_center[1]-180 <0) :
        angle = 90
    
    elif (template_center[0]-320 == 0 and template_center[1]-180 >0) :
        angle = 270
    
    elif (template_center[0]-320 <0 and template_center[1]-180 == 0) :
        angle = 180
    
    else :
        angle = 0
    
    if angle == 360:
        angle = 0

    '''
    if (template_center[0] == 320):
        if (template_center[1] == 180):
            angle = 0
        elif (template_center[1] < 180):
            angle = 90
        else :
            angle = 270

    elif (template_center[1] == 180):
        if (template_center[0] == 320):
            angle = 0
        elif (template_center[0] < 320):
            angle = 180
        else :
            angle = 270
    else :
        angle = math.degrees(math.atan((template_center[1] - 180)/(template_center[0] - 320)))
        if (angle > 0 and ((template_center[1] - 180) < 0 and (template_center[0] - 320) <0)):
            angle = 180+angle
    
        if (angle < 0 and ((template_center[1] - 180) > 0 and (template_center[0] - 320) <0)):
            angle = 180+angle
        
        if (angle < 0 and ((template_center[1] - 180) < 0 and (template_center[0] - 320) >0)):
            angle = 360+angle
    '''
    '''
    #See from here
    if (template_center[0] != 320):
        if ((template_center[1] - 180) < 0 and (template_center[0] - 320) <0 ):
            angle = 180+ angle
    
        if ((template_center[1] - 180) < 0 and (template_center[0] - 320) >0):
            angle = 360 - angle

        if ((template_center[1] - 180) > 0 and (template_center[0] - 320) <0):
            angle = 180 - angle
    '''
    #print template_center
    cv2.rectangle(rgb, top_left, bottom_right, (0, 255, 0), 2)
    cv2.line(rgb, (320, 180), template_center, (255, 120, 120), 2, cv2.CV_AA)

    cv2.line(rgb, (0, 120), (640, 120), (255, 0, 255), 1,  cv2.CV_AA)
    cv2.line(rgb, (0, 240), (640, 240), (255, 0, 255), 1,  cv2.CV_AA)
    cv2.line(rgb, (214, 0), (214, 360), (255, 0, 255), 1,  cv2.CV_AA)
    cv2.line(rgb, (428, 0), (428, 360), (255, 0, 255), 1,  cv2.CV_AA)
    cv2.circle(rgb, (320, 180), 2, (255, 255, 0), 2, cv2.CV_AA)

    ang.data = angle
    d.data = dist

    dist_pub.publish(d)
    angle_pub.publish(ang)

    cv2.imshow("Matched Template : ", rgb)
    cv2.waitKey(1)


