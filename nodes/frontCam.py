'''
Dt: 7/09/2016 : Wednesday 
ROS Node for getting the Video Feed from the Front Camera of the Drone
ROS Node Name           : DFC (Drone Front Camera)
ROS Subsribed to Topic  : "/ardrone/image_rect_color"
ROS Callback Method     : callback()
ROS Comm Frequency      : 1hz
Mono Image              : frame_mono
Color Image             : frame_color
'''

import rospy
import cv2
import Queue
import time
import numpy as np
from threading import Thread
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def callback(data):
    frame_color = bridge.imgmsg_to_cv2(data, "bgr8")
    frame_mono  = bridge.imgmsg_to_cv2(data, "mono8")
    cv2.imshow('Drone video Feed', frame_mono)
    cv2.imshow('Drone video Feed', frame_color)
    cv2.waitKey(1)



def getVideo():
    rospy.Rate(1)
    #self.image_sub = rospy.Subscriber('/ardrone/image_rect_color', Image, self.callback)
    image_sub = rospy.Subscriber('/ardrone/front/image_raw', Image, callback)
    print 'Getting Video Feed . . . ' 
    #rospy.sleep(0.3)
    #return self.frame_mono
    try :
        rospy.spin()
    except KeyboardInterrupt :
        print "Shutting Down"

'''
class frontCam :
    def __init__(self):
        #Thread.__init__(self)
        self.height, self.width, self.ch = 0, 0, 0
        self.frame_color, self.frame_mono = np.zeros((640, 360, 3), dtype = 'uint8'), np.zeros((640, 360, 1), dtype = 'uint8')
        self.bridge = CvBridge()
        #fourcc =  cv2.CV_FOURCC(*'XVID')
        self.path = '/home/siddhartha-drone/drone_video/DroneVideo_'
        self.time_stamp = str(int(time.time()))
        self.extension = '.avi'
        #self.video_path = self.path+self.time_stamp+self.extension
        #self.out = cv2.VideoWriter(self.video_path, fourcc, 30, (640, 360), True)
        #self.out = cv2.VideoWriter('/home/siddhartha-drone/drone_video/DroneVideo1.avi', fourcc, 30, (640, 360), True)
        print "Innitial Done"
        self.start_time = int(time.time())
        #self.threadLock = threading.Lock()
        #self.q_in = Queue.Queue()
        #self.q_in = q_in
        #self.getVideo()

    def run(self):
        #self.threadLock.acquire()
        print "Just to 3"
        self.getVideo()
        print "Just to 4"
        #self.threadLock.release() 

    def getVideo(self) :
        rospy.Rate(1)
        #self.image_sub = rospy.Subscriber('/ardrone/image_rect_color', Image, self.callback)
        self.image_sub = rospy.Subscriber('/ardrone/front/image_raw', Image, self.callback)
        print 'Getting Video Feed . . . ' 
        #rospy.sleep(0.3)
        #return self.frame_mono
        try :
            rospy.spin()
        except KeyboardInterrupt :
            print "Shutting Down"
    
    def callback(self, data) :
        #print "Thread 2"
        self.frame_color = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.frame_mono  = self.bridge.imgmsg_to_cv2(data, "mono8")
        #self.out.write(self.frame_color)
        cv2.imshow('Drone video Feed', self.frame_mono)
        cv2.waitKey(1)
        t = int(time.time()) - self.start_time
        if (t >10 and t<30 ):
            self.out.write(self.frame_color)
        if (t > 32):
            rospy.signal_shutdown("Done")
        #q_in.put()
        #return self.frame_mono
        #self.vanishPoint()
        
'''