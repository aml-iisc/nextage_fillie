

# Print "Hello!" to terminal

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

import os
import struct
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import ros_numpy
import math
# import ellipsis as el


print("Hello3!")

rospy.init_node('munjal_image_test', anonymous=True)
rospy.loginfo("Hello ROS!")

bridge = CvBridge()
num = 0
# right_image = 0
left_image = 0
point_cloud= 0
flag = 0
global final_xyz
# final_xyz=0

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# plt.ion()
# plt.show()
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
    # global flag
    # print("hii")
    # # ax.cla()
    # if(flag==6):
    #     point_array = ros_numpy.point_cloud2.pointcloud2_to_array(point_cloud_msg,squeeze=False)
    #     # print(point_array.shape)
    #     xyz_array = ros_numpy.point_cloud2.get_xyz_points(point_array,remove_nans=False)
    #     # print(xyz_array.shape)
    #     # print(point_array['rgb'].shape)
    #     rgb_data = point_array['rgb'].astype(np.float32)
    #     # rgb_data *= 255 # or any coefficient
    #     # I = I.astype(np.uint8)
    #     # print(type(rgb_data[0][0]))
    #     # print(rgb_data[0][0])  
    #     rgba_data = rgb_data.view((np.uint8, 4))
    #     # print(rgba_data[0][0])  
    #     # data_reshaped = rgba_data.reshape(rgba_data.shape[0], rgba_data.shape[1], rgba_data.shape[2])

    #     # rgba_data = rgb_data.astype(np.uint8)
    #     # uint8_matrix_split = np.unpackbits(rgba_data,axis=-1).reshape((1096,1936,8))
    #     # rgba_data = rgba_data.reshape((1096,1936,4))
    #     # print(rgba_data.shape)
    #     xyz_flat = xyz_array.reshape(-1, 3)
    #     fig = plt.figure(figsize=(10, 7))
    #     ax = fig.add_subplot(111, projection='3d')

    #     # R = (rgb_data[:, :] * 255).astype(np.uint8)
    #     # G = (rgb_data[:, :] * 255).astype(np.uint8)
    #     # B = (rgb_data[:, :] * 255).astype(np.uint8)

    #     # # Flatten the arrays to create a list of RGB values
    #     # R_flat = R.flatten()
    #     # G_flat = G.flatten()
    #     # B_flat = B.flatten()
    #     # ax.plot(xyz_flat[:, 0], xyz_flat[:, 1], xyz_flat[:, 2], c=np.stack([R_flat, G_flat, B_flat], axis=-1), marker='o', alpha=0.5)
    #     # ax.plot(xyz_flat[:, 0], xyz_flat[:, 1], xyz_flat[:, 2], c=rgba_data[:,:,:3]/255, marker='o', alpha=0.5)
    #     ax.scatter(xyz_flat[:, 0], xyz_flat[:, 1], xyz_flat[:, 2],c=xyz_flat[:, 2], cmap='viridis', marker='o', alpha=0.5)
    #     ax.set_xlabel('X axis')
    #     ax.set_ylabel('Y axis')
    #     ax.set_zlabel('Z axis')

    #     # Set title
    #     ax.set_title('Dynamic 3D Visualization with RGB Colors')
    #     plt.show()
    # flag=flag+1


    global point_cloud
    global flag
    global final_xyz
    # print("hii")
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)
    # if(flag==26):
        # print(ord(point_cloud_msg.data[646865]))
        # print(float.from_bytes(point_cloud_msg.data[0:5],byteorder='little',signed=True))
        # str1 = bytearray(point_cloud_msg.data[619520:619524])
        # # print(str1)
        # print(struct.unpack('<f',str1))
    data_array = np.frombuffer(point_cloud_msg.data, dtype=np.uint8)
    # print(point_cloud_msg.point_step)
    # print(data_array.shape)
    # print(point_cloud_msg.fields)
    data_array = data_array.reshape((1096,1936,32))
    data_array = data_array.view(np.float32)
    # print(data_array.shape)
    x = data_array[:, :, 0]
    y = data_array[:, :, 1]
    z = data_array[:, :, 2]
    # extra_floats1 = data_array[:, :, 3*float_size:].astype(dtype=np.float32).reshape((image_height, image_width, 8 - 3))
    final_matrix = np.stack((x, y, z), axis=-1)
    # print(final_matrix.shape)
    final_xyz = final_matrix
    xyz_points = final_matrix.reshape(-1, 3)

    # Extract X, Y, Z coordinates
    X = xyz_points[:, 0]
    Y = xyz_points[:, 1]
    Z = xyz_points[:, 2]

    # Create a 3D scatter plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the points
    sc = ax.scatter(X, Y, Z, c=Z, cmap='viridis', marker='o', alpha=0.5)

    # Add color bar which maps values to colors
    plt.colorbar(sc)

    # Set labels
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Set title
    ax.set_title('3D Point Cloud Visualization')

        # Show plot
        # plt.show()
    # flag=flag+1
    # print("hii")
    # Try to convert the ROS Image message to a CV2 Image
    # try:
    #     point_cloud = bridge.(img_msg, "bgr8")
    # except CvBridgeError, e:
    #     rospy.logerr("CvBridge Error: {0}".format(e))


# def image_callback_right(img_msg):
#     global right_image
#     # log some info about the image topic
#     # rospy.loginfo(img_msg.header)

#     # Try to convert the ROS Image message to a CV2 Image
#     try:
#         right_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
#     except CvBridgeError, e:
#         rospy.logerr("CvBridge Error: {0}".format(e))

   

    


# sub_image1 = rospy.Subscriber("/left/image_raw", Image, image_callback_left)
sub_image1 = rospy.Subscriber("/left/image_rect_color", Image, image_callback_left)
points_c = rospy.Subscriber("/points2", PointCloud2, point_cloud_callack)
# plt.show()
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
        segmented_image = cv2.imread(segmented_image_path,0)
        print(segmented_image.shape)
        segmented_image_rs = cv2.resize(segmented_image, (width, 480))
        # final_xyz[se]
        print(final_xyz.shape)
        cv2.imshow('segmented_image',segmented_image_rs)
        x=0
        y=0
        z=0
        count=0
        for i in range(1096):
            for j in range(1936):
                # print(segmented_image[i][j])
                math.isnan(x)
                if segmented_image[i][j]>0 and (not math.isnan(final_xyz[i][j][0])) and (not math.isnan(final_xyz[i][j][1])) and (not math.isnan(final_xyz[i][j][2])):
                    x = x + final_xyz[i][j][0]
                    y = y + final_xyz[i][j][1]
                    z = z + final_xyz[i][j][2]
                    count = count+1
        avg_x = x/count
        avg_y = y/count
        avg_z = z/count
        print(avg_x,avg_y,avg_z)  
        # segmented_image_rs = cv2.resize(segmented_image, (width, 480))
        # # final_xyz[se]
        # cv2.imshow('segmented_image',segmented_image_rs)
        os.remove(command_file_path)
        os.remove(segmented_image_path)
        # num += 1
    #"/home/mj/catkin_ws/src/camera_calib/scripts/send_image.py"
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