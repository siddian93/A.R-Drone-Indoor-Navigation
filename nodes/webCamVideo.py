import cv2
import numpy as np
import rospy


def getVideo() :
	vid = cv2.VideoCapture(0)
	while (True) :
		ret, frame = vid.read()
		cv2.imshow("FRAME" , frame)
		cv2.waitKey(1)

