'''
Dt: 9/09/2016 : Friday 
ROS Node for Getting The VanishPoint fromn the Incomming Drone Video Feed
ROS Node Name           : VPN (Vanish Point)
ROS Subsribed to Topic  : "/ardrone/image_rect_color"
ROS Callback Method     : callback()
ROS Comm Frequency      : 1hz
Mono Image              : frame_mono
Color Image             : frame_color
Script                  : vanishPoint
Threading               : callback and findVanishPoint
Message Passing         : Deque : q_in and q_out
'''

import rospy
import cv2
import time
import math
import numpy as np
from collections import deque
from threading import Thread
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class vanishPointFound():
	flag = False


class vanishPoint(Thread) :
    def __init__(self) :
        Thread.__init__(self)
        self.q = deque(maxlen=2)
        self.q_in = deque(maxlen=2)
        self.q_out = deque(maxlen=2)
        self.line_coord = np.zeros((1, 4))
        self.bridge = CvBridge()
        fourcc =  cv2.cv.CV_FOURCC(*'XVID')
        self.out = cv2.VideoWriter('/home/siddhartha-drone/drone_video/DroneVideo1.avi', fourcc, 30, (640, 360), True)

    def getVideo(self, q_in):
        rospy.Rate(1)
        self.q_in = q_in
        self.image_sub = rospy.Subscriber('/ardrone/image_rect_color', Image, self.callback)
        print 'Getting Video Feed . . . '
        try :
            rospy.spin()
        except KeyboardInterrupt :
            print "Shutting Down"
    
    def callback(self, data):
        #print "Thread 2"
        self.frame_color = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.frame_mono  = self.bridge.imgmsg_to_cv2(data, "mono8")
        cv2.imshow('Drone video Feed', self.frame_mono)
        cv2.waitKey(1)
        self.q_in.append(self.frame_mono)
        #time.sleep(0.5)

    

    def findVanishPoint(self, q_out) :
        while(True):
            #print "Thread 1"
            self.q_out = q_out
            line_coord = np.zeros((1,2))
            intersect_p = np.zeros((1, 2))
            G = {}
            t1 = time.time()
            if (len(q_out)>0):
                self.img = self.q_out.pop()
                #self.black = np.zeros((360, 640, 3), dtype = 'uint8')
                if (np.count_nonzero(self.img) >0 or self.img !=None):
                    gray = cv2.GaussianBlur(self.img,(3,3),0)
                    gray = cv2.Canny(gray,20,6*10, apertureSize = 3)
                    #self.img = gray
                    hough_linesP= cv2.HoughLinesP(gray, 1, np.pi/180, 100, np.array([]), 100, 10)[0]
                    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                    
                    line_coord = np.delete(line_coord, 0, 0)
                    intersect_p = np.delete(intersect_p, 0, 0)
                    
                    for x1, y1, x2, y2 in hough_linesP :
                        if x1 == x2 :
                            continue
                        m = (1.0*(y2-y1))/(1.0*(x2-x1))
                        c = float(y1) - (m*float(x1))
                        if (m == 0) :
                            continue
                        Point_A = (int(-c/m), 0)
                        if m < 0 :
                            Point_B = (0, int(c))
                        else :
                            Point_B = (640, int(m*640+c))
						
                        p_temp = [[m, c]]
                        line_coord = np.append(line_coord, p_temp, axis = 0)
                        cv2.line(gray, Point_A, Point_B, (0, 255, 0), 1, 8)
                    
                    l = len(line_coord)

                    for i in range(l):
						for j in range(i, l) :
							if (i==j) :
								continue
							m1 = line_coord[i][0]
							m2 = line_coord[j][0]
							
							if m1 == m2 :
								continue
							
							c1 = line_coord[i][1]
							c2 = line_coord[j][1]
							
							x =  (c2 - c1) / (m1 - m2)
							y = float(m2)*x + c2
							intersect_p = np.append(intersect_p, [[x, y]], 0)
							
							if ((x < 0  and x > 640) and (y< 0 and y > 360)) :
								continue

							a , b = int(x*11/640), int(y*11/360)
							cell = 10*a + b 
							
							if G.has_key(cell) :
								G[cell] += 1
							else :
								G[cell] = 1
                        

                    if G == {} :
                        self.vpFound = False
                        continue
                    max_occ = max(G, key=G.get)
                    Gab = G[max_occ]
                    #print Gab
                    loc_x = int(max_occ/10)
                    loc_y = int(max_occ%10)
                    xv, yv = (640*(loc_x+0.5))/11, (360*(loc_y+0.5))/11
                    vanish_p = (int(xv), int(yv))

                    x_s, y_s , N = 0, 0, 0

                    for xs, ys in intersect_p :
						d = ((xs-xv)*(xs-xv)) + ((ys-yv)*(ys-yv))
						d = math.sqrt(d)
						if d < 100 :
							x_s +=xs
							y_s +=ys
							N +=1
                    if N==0:
                        continue
                    xv_new , yv_new = x_s/N, y_s/N

                    variance, distance = 0.0, 0.0
                    for xs, ys in intersect_p :
                        if N!=0 :
							d = ((xs-xv)*(xs-xv)) + ((ys-yv)*(ys-yv))
							d = math.sqrt(d)
                            distance +=d
							if d < 100 :
								variance += np.square(xv_new - xs) + np.square(yv_new-ys) 
						
                    if N!=0 :
                        variance = variance/N
                        std_dev = np.sqrt(variance)
                        mean = distance/N
					
                    #print std_dev

                    Prob = (1/(2*math.pi*variance))*math.exp(np.square(xv_new - mean)/(2*variance))
                    print Prob
                    vanish_new = (int(xv_new), int(yv_new))

                    self.vpFound = True
                    cv2.circle(gray, vanish_new, 4, (0, 255, 255), 10)
                    self.out.write(gray)
                    cv2.imshow("Detected Lines", gray)
                    cv2.waitKey(15)
						    

                    
    
    def run_threads(self) :
        t1 = Thread(target=self.getVideo, args=(self.q,))
        t2 = Thread(target=self.findVanishPoint, args=(self.q,))
        t1.start()
        time.sleep(2)
        t2.start()



'''
    def extendLine(self, x1, y1, x2, y2):
        m = (((y2-y1)*1.0)/((x2-x1)*1.0))
        if  (x2-x1) != 0:
            c = y1-m*x1
            x1, x2 = 0.0, 640.0
            y1 = m*x1+c
            y2 = m*x2+c
        else :
            y1, y2, m,  c = 0, 360, 'p', 0
        return x1, y1, x2, y2, m, c
    
    def intersect(self, l1, l2):	
		if (l1[4] == 'p' and l2[4] != 'p') :
			x = float(l1[0])
			y = (float(l2[4])* float(l1[0])) + float(l2[5])
			#if ((x <= 640 and x>= 0) and (y <= 360 and y >=0)):
			#	return x, y
            return x, y	
			#else :
			#	return 'p', 'p'
        
		elif (l2[4] == 'p' and l1[4] != 'p') :
			
			x = float(l2[0])
			y = (float(l1[4]) * float(l2[0])) + float(l1[5])
			#if ((x <= 640 and x>= 0) and (y <= 360 and y >=0)):
			#	return x, y
            return x, y
			#else :
			#	return 'p', 'p'

		
		elif (( l1 != l2) and (l1[4] !='p' and l2[4] != 'p') ):
			if ((float(l1[4])-float(l2[4])>0) or (float(l1[4])-float(l2[4]) < 0)) :
				x = (float(l2[5]) - float(l1[5]))/(float(l1[4])-float(l2[4]))
				y = float(l1[4])*float(l1[0]) + float(l1[5])
				#if ((x <= 640 and x>= 0) and (y <= 360 and y >= 0)):
				#	return x, y
                return x, y
				#else :
				#	return 'p', 'p'
			else :
				return 'p', 'p'
		
		else :
			return 'p', 'p'
    
'''
'''
    def intersect(self, l1, l2):
        if (l1 != l2) :
            x = (float(l2[5]) - float(l1[5]))/(float(l1[4])-float(l2[4]))
            y = float(l1[4])*float(l1[0]) + float(l1[5])
            if ((x < 640 and x> 0) and (y < 360 and y >0)):
                return x, y
            else :
                return 'p', 'p'
        elif (l1[4] == 'p') :
            x = l1[0]
            y = l2[4]*x+l2[5]
            return x, y
        
        elif (l2[4] == 'p')
            x = l2[0]
            y = l1[4]*x+l1[5]
            return x, y


        else :
            return 'p', 'p'
    '''

'''
                    for x1, y1, x2, y2, m1, c1 in line_coord :
                        for x_1, y_1, x_2, y_2, m2, c2 in line_coord:
                            #if ((m1 != 'p') and (m2 !='p') and (float(m1) != float(m2))) :
                            if (m1 == -0 or m2 == -0):
								m1, m2 = float(m1), float(m2)
                            if (m1 != m2) :
                                l1 = [x1, y1, x2, y2, m1, c1]
                                l2 = [x_1, y_1, x_2, y_2, m2, c2]
                                #self.intersect(l1, l2)
                                x, y = self.intersect(l1, l2)
                                #print x, y
                                if (x != 'p' and y!='p'):
									int_p = [[x, y]]
									intersect_p = np.append(intersect_p, int_p, axis = 0)
                    Gab = np.zeros((11, 11))
                    for x, y in intersect_p :
                        #xd = int((x*1.0)*0.0171875)
                        #yd = int((y*1.0)*0.0305556)
                        xd = int(x*11/640)
                        yd = int(y*11/320)
                        if (xd<11 and yd<11):
                            Gab[xd][yd]+=1
                    #print Gab
                    #ind = np.where(Gab == Gab.max())
                    comp, loc_R, loc_C = 1, 5, 5
                    for i in range(3,8) :
                        for j in range(3,8):
                            if (Gab[i][j]>comp):
                                comp = Gab[i][j]
                                loc_R = i
                                loc_C = j

                    #xv, yv = 58.181819*(loc_C+0.5), 32.727273*(loc_R+0.5)
                    xv, yv = (640*loc_C)/11, (320*loc_R)/11 
                    xv, yv = int(xv), int(yv)
                    N = 0
                    x_s, y_s = [0], [0]
					
                    for xs, ys in intersect_p :
						d = ((xs-xv)*(xs-xv)) + ((ys-yv)*(ys-yv))
						d = math.sqrt(d)
						if d<100 :
							N+=1
							x_s.append(xs)
							y_s.append(ys)
                    x_s.pop(0)
                    y_s.pop(0)
                    xv_new, yv_new = 0, 0
                    for x_t in x_s :
					    if N!=0 :
						    xv_new +=x_t
					
                    for y_t in y_s :
					    if N!=0 :
						    yv_new+=y_t

                    if N!=0 :
					    yv_new = int(yv_new/N)
					    xv_new = int(xv_new/N) 
                    
                    #if (xv_new == 0 and yv_new == 0):
                    #      xv_new, yv_new = 320, 180
                    print Gab
                    if N!=0 :
                        cv2.circle(gray, (xv_new, yv_new), 5, (255, 0, 0, ), 20)
                    #print xv, yv    
                    cv2.imshow("Detected Lines", gray)
                    #self.out.write(self.frame_color)
                    cv2.waitKey(1)
                    self.out.write(gray)
                    del gray
                    #del self.black
                    del self.q_out
                    #time.sleep(0.0)
                    #print time.time() -t1
                    '''

        
