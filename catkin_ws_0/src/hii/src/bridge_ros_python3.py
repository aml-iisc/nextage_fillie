#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
print("hiii")

print("Hello3!")

rospy.init_node('hii', anonymous=True)
rospy.loginfo("Hello ROS!")
print("hurr")