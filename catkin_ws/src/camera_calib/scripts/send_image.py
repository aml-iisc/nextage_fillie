

# Print "Hello!" to terminal

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import os

print("Hello3!")

rospy.init_node('munjal_image_test', anonymous=True)
rospy.loginfo("Hello ROS!")

bridge = CvBridge()
num = 0
# right_image = 0
left_image = 0
point_cloud= 0
# def show_image_left(img):
#     cv2.imshow("Image Window Left", img)
#     cv2.waitKey(3)

# def show_image_right(img):
#     cv2.imshow("Image Window Right", img)
#     cv2.waitKey(3)

def image_callback_left(img_msg):
    global left_image
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        left_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

def point_cloud_callack(point_cloud_msg):
    global point_cloud
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        point_cloud = bridge.(img_msg, "bgr8")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))


# def image_callback_right(img_msg):
#     global right_image
#     # log some info about the image topic
#     # rospy.loginfo(img_msg.header)

#     # Try to convert the ROS Image message to a CV2 Image
#     try:
#         right_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
#     except CvBridgeError, e:
#         rospy.logerr("CvBridge Error: {0}".format(e))

   

    


sub_image1 = rospy.Subscriber("/left/image_rect_color", Image, image_callback_left)
sub_image1 = rospy.Subscriber("/points2", PointCloud2, image_callback_left)

# sub_image2 = rospy.Subscriber("/right/image_raw", Image, image_callback_right)

# cv2.namedWindow("Image Window Left", 1)
# # cv2.namedWindow("Image Window Right", 1)

# cv2.waitKey(5000)
ratio = float(1936.0)/1096.0
# print(ratio)
width = int(480*ratio)
while not rospy.is_shutdown():
    k = cv2.waitKey(5)
    # print(k)
    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        prompt = raw_input("Please input your prompt: ")
        file = open("../../send/this_is_the_prompt.txt","w")
        L = [prompt]
        file.writelines(L)
        file.close()
        cv2.imwrite('../../send/please_segment.png',left_image)
        file = open("../../send/do_segment.txt","w")
        file.close()
        # cv2.imwrite('images/stereoLeft/imageL' + str(num) + '.png', left_image)
        # cv2.imwrite('images/stereoRight/imageR' + str(num) + '.png', right_image)
        print("images saved!")
        command_file_path = "../../receive/segmentation_done.txt"
        segmented_image_path = '../../receive/segmented.png'
        while not (os.path.exists(segmented_image_path) and os.path.exists(command_file_path)):
            pass
        segmented_image = cv2.imread(segmented_image_path)
        segmented_image_rs = cv2.resize(segmented_image, (width, 480))
        cv2.imshow('segmented_image',segmented_image_rs)
        os.remove(command_file_path)
        os.remove(segmented_image_path)
        # num += 1
    # print("hii")
    # print(np.shape(left_image),np.shape(right_image))
        # print(width)
    imSL = cv2.resize(left_image, (width, 480))
    # imSR = cv2.resize(right_image, (width, 480))
    # numpy_horizontal = np.hstack((imSL, imSR))
    # cv2.imshow('Img R',right_image)
    cv2.imshow('Img L',imSL)
        # cv2.imshow('IMG L vs R', numpy_horizontal)
    
    # rospy.spin()
cv2.destroyAllWindows()