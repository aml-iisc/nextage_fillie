import cv2
import numpy as np
import glob
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from sensor_msgs.msg import Image
import signal
import sys

print("Hello3!")

rospy.init_node('munjal_image_test', anonymous=True)
rospy.loginfo("Hello ROS!")

bridge = CvBridge()
# num = 0
# right_image = 0
left_image = 0
img_array = []
size = (1096,1936)
cnt = 0
def image_callback_left(img_msg):
    global left_image
    global img_array
    global cnt
    # Try to convert the ROS Image message to a CV2 Image
    try:
        left_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
        cv2.startWindowThread()
        cv2.namedWindow('Live Image HEAD')
        cv2.imshow('Live Image HEAD',left_image)
        cv2.imwrite('/home/rahul_birthday/img_0.png',left_image)
        cnt=  cnt+1    
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))


# for filename in glob.glob('*.png'):
#    img = cv2.imread(filename)
#    height, width, layers = img.shape
#    size = (width,height)
#    img_array.append(img)

def shutup(sig,frame):
    # for i in range(len(img_array)):
    #     out.write(img_array[i])
    # out.release()
    sys.exit(0)

signal.signal(signal.SIGINT,shutup)
sub_image1 = rospy.Subscriber("/left/image_raw", Image, image_callback_left)

# out = cv2.VideoWriter('/home/rahul_birthday/video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
while not rospy.is_shutdown():
    pass