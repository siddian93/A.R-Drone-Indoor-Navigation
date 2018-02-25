import rospy
import cv2
import math
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float64
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
dev_pub = rospy.Publisher('/ardrone/str_dev', Float64, queue_size = 1)

def climb_stairs():
    rospy.Rate(1)
    img_sub_color = rospy.Subscriber('/ardrone/image_rect_color', Image, callback_color)
    #img_sub_mono = rospy.Subscriber('ardrone/image_rect', Image, callback_mono)
    try : 
        rospy.spin()
    except KeyboardInterrupt :
        print 'Shutting Down'

def callback_color(data):
    img = bridge.imgmsg_to_cv2(data)
    gray = bridge.imgmsg_to_cv2(data, 'mono8')
    #print gray.shape
    [im_l, im_w, l] = gray.shape
    dev = im_w/2
    gray = cv2.GaussianBlur(gray,(3,3),0)
    gray = cv2.Canny(gray, 20, 6*10, apertureSize = 3)
    hough_linesP= cv2.HoughLinesP(gray, 1, np.pi/180, 100, np.array([]), 100, 10)[0]
    st = []
    slope_avg = 0.0 
    for x1, y1, x2, y2 in hough_linesP :
        if x1 == x2:
            continue
        slope = math.degrees(((y1-y2)*1.0)/((x1-x2)*1.0))
        if slope < -40 or slope > 40 :
            continue
        else :
            #print slope
            st.append([x1, y1, x2, y2])
            slope_avg+=slope
            #cv2.line(gray, (x1, y1), (x2, y2), (255, 0, 255), 1, cv2.CV_AA)
        #print slope


    #####Sort the Points based on the Y1 Value
    l = len(st)
    for i in range(l):
        for j in range (l) :
            if (st[i][1]>st[j][1]):
                temp = st[j]
                st[j] = st[i]
                st[i] = temp
                #print temp


    ######## Find the Difference in the line sparcity
    dist = []
    for i in range (l-1):
        dist.append(st[i][1] - st[i+1][1])
        #dist[i] = st[i][1] - st[i+1][1] 
        #print st[i], dist[i]



    ####Find Stair Clusters

    for i in range(l-1):
        if (dist[i]> 50):
            continue
        else :
            #pass
            #cv2.line(gray, (st[i][0], st[i][1]), (st[i][2], st[i][3]), (255, 255, 0), 1, cv2.CV_AA)
            cv2.line(gray, (st[i][0], st[i][1]), (st[i][2], st[i][3]), (255, 255, 0), 1)

    #######Find the The mean of the Lines End Points
    avg_x_begin = 0
    avg_x_end = 0
    for points in st:
        avg_x_begin +=points[0]
        avg_x_end +=points[2]
    
    if len(st) != 0:    
        avg_x_begin /=len(st)
        avg_x_end /=len(st)
        avg = (avg_x_begin+avg_x_end)/2
        slope_avg /=len(st)
        dev = (im_w/2)-avg
        #print slope_avg
        cv2.line(img, (avg_x_begin, 0), (avg_x_begin, 360), (255, 0, 0), 1)
        cv2.line(img, (avg_x_end, 0), (avg_x_end, 360), (255, 0, 0), 1)
        cv2.line(img, (avg, 0), (avg, 360), (0, 255, 0), 1)
        cv2.line(img, (im_w/2, 0), (im_w/2, 360), (0, 0, 255), 1)
        
    #cv2.line(gray, (avg_x_begin, 0), (avg_x_begin, 360), (255, 0, 0), 1, cv2.CV_AA)
    #cv2.line(gray, (avg_x_end, 0), (avg_x_end, 360), (255, 0, 0), 1, cv2.CV_AA)
    #cv2.line(gray, (avg, 0), (avg, 360), (0, 255, 0), 1, cv2.CV_AA)
    #cv2.line(gray, (im_w/2, 0), (im_w/2, 360), (0, 0, 255), 1, cv2.CV_AA)

    print dev
    dev_pub.publish(dev)
    cv2.imshow("Staircase",gray)
    cv2.imshow("Original", img)
    #cv2.waitKey(0)
    #cv2.imshow('Frame Color', gray)
    cv2.waitKey(1)

def callback_mono(data):
    img = bridge.imgmsg_to_cv2(data)
    cv2.imshow('Frame Mono', img)
    cv2.waitKey(1)
