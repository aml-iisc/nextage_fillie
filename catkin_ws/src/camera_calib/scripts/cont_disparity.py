import cv2
import numpy as np 
import glob
from tqdm import tqdm
import PIL.ExifTags
import PIL.Image
from matplotlib import pyplot as plt 

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

rospy.init_node('opencv_example', anonymous=True)
rospy.loginfo("Hello ROS!")
right_image = 0
left_image = 0
bridge = CvBridge()



# Downsamples image x number (reduce_factor) of times. 
def downsample_image(image, reduce_factor):
	for i in range(0,reduce_factor):
		#Check if image is color or grayscale
		# print(image.shape)
		if len(image.shape) > 2:
			row,col = image.shape[:2]
		else:
			row,col = image.shape
		# print(row,col)
		image = cv2.pyrDown(image, dstsize= (col//2, row // 2))
	return image

def image_callback_left(img_msg):
    global left_image
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        left_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    

def image_callback_right(img_msg):
    global right_image
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        right_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))


sub_image1 = rospy.Subscriber("/left/image_raw", Image, image_callback_left)
sub_image2 = rospy.Subscriber("/right/image_raw", Image, image_callback_right)

#=========================================================
# Stereo Calibration and rectification
#=========================================================
# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

Q = cv_file.getNode('q').mat()

# # imgL = cv2.imread('images/stereoLeft/imageL24.png')
# # imgR = cv2.imread('images/stereoRight/imageR24.png')

block_size = 11
min_disp = -25
# max_disp = 31
# Needs to be divisible by 16
range_disp = 288

max_disp = range_disp - min_disp 
# Create Block matching object. 
stereo = cv2.StereoSGBM_create(minDisparity= min_disp,
	numDisparities = range_disp,
	blockSize = block_size,
	uniquenessRatio = 5,
	speckleWindowSize = 5,
	speckleRange = 5,
	disp12MaxDiff = 2,
	P1 = 8 * 3 * block_size**2,#8*img_channels*block_size**2,
	P2 = 32 * 3 * block_size**2) #32*img_channels*block_size**2)

stereo = cv2.StereoBM_create(numDisparities=range_disp,blockSize=block_size)

while not rospy.is_shutdown():
    while not (np.shape(left_image)==(1096,1936,3) and np.shape(right_image) == (1096,1936,3)):
        pass 
    k = cv2.waitKey(1)
    imgL = downsample_image(left_image,0)
    imgR = downsample_image(right_image,0)

    # ratio = float(1936.0)/1096.0
    # # print(ratio)
    # width = int(480*ratio)
    # imSL = cv2.resize(imgL, (width, 480))
    # imSR = cv2.resize(imgR, (width, 480))

    # imgL = cv2.imread('trash/imageL8.png')
    # imgR = cv2.imread('trash/imageR8.png')
    # imgL = downsample_image(imgL,1)
    # imgR = downsample_image(imgR,1)
    # Show the frames
    cv2.imshow("frame right", right_image) 
    cv2.imshow("frame left", left_image)

    # h=cv2.waitKey(0)


    # Undistort and rectify images
    imgR = cv2.remap(imgR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    imgL = cv2.remap(imgL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                
    # # Show the frames
    cv2.imshow("frame right undistorted", imgR) 
    cv2.imshow("frame left undistorted", imgL)
    # # cv2.waitKey(0)

    # # Downsample each image 3 times (because they're too big)
    imgL = downsample_image(imgL,0)
    imgR = downsample_image(imgR,0)

    imgLgray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    imgRgray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    # Show the frames
    # cv2.imshow("frame right downscaled", imgR) 
    # cv2.imshow("frame left downscaled", imgL)

    disparity_map = stereo.compute(imgLgray, imgRgray)
    norm_image = cv2.normalize(disparity_map, None, alpha = 0, beta = 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    cv2.imshow("disparity", norm_image)
    # print(disparity_map.shape)
    # Show disparity map before generating 3D cloud to verify that point cloud will be usable. 
    # plt.imshow(disparity_map,'gray')
    # plt.show()
	# cv2.waitKey(0)


#=========================================================
# Create Disparity map from Stereo Vision
#=========================================================

# For each pixel algorithm will find the best disparity from 0
# Larger block size implies smoother, though less accurate disparity map

# Set disparity parameters
# Note: disparity range is tuned according to specific parameters obtained through trial and error. 


#stereo = cv2.StereoBM_create(numDisparities=num_disp, blockSize=win_size)

# Compute disparity map
# disparity_map = stereo.compute(imgLgray, imgRgray)

# print(disparity_map.shape)
# # Show disparity map before generating 3D cloud to verify that point cloud will be usable. 
# plt.imshow(disparity_map,'gray')
# plt.show()


# #=========================================================
# # Generate Point Cloud from Disparity Map
# #=========================================================

# # Get new downsampled width and height 
# h,w = imgR.shape[:2]

# # Convert disparity map to float32 and divide by 16 as show in the documentation
# print(disparity_map.dtype)
# disparity_map = np.float32(np.divide(disparity_map, 16.0))
# print(disparity_map.dtype)
# print(Q)
# # Q = np.float32([[1, 0, 0, 0],
# # 				[0, -1, 0, 0],
# # 				[0, 0, 1914.96258*0.05, 0],
# # 				[0, 0, 0, 1]])

# print(Q)
# # Reproject points into 3D
# # point_s_gen3D = np.array(137,242,3)
# # for x in range(242):
# # 	for y in range(137):
# # 		point_s_gen3D[y][x]= [x+Q[0][3],y+Q[1][3],]
# points_3D = cv2.reprojectImageTo3D(disparity_map, Q, handleMissingValues=False)
# # Get color of the reprojected points
# colors = cv2.cvtColor(imgR, cv2.COLOR_BGR2RGB)
# print(points_3D.shape,colors.shape)
# print(points_3D[0][0])
# # Get rid of points with value 0 (no depth)
# print(disparity_map[0][0])
# print(disparity_map.min())
# mask_map = disparity_map > disparity_map.min()
# print(mask_map.shape)
# # Mask colors and points. 
# output_points = points_3D[mask_map]
# output_colors = colors[mask_map]
# print(output_points.shape,output_colors.shape)
# print(output_points[0],output_colors[0])

# # Function to create point cloud file
# def create_point_cloud_file(vertices, colors, filename):
# 	colors = colors.reshape(-1,3)
# 	vertices = np.hstack([vertices.reshape(-1,3),colors])

# 	ply_header = '''ply
# 		format ascii 1.0
# 		element vertex %(vert_num)d
# 		property float x
# 		property float y
# 		property float z
# 		property uchar red
# 		property uchar green
# 		property uchar blue
# 		end_header
# 		'''
# 	with open(filename, 'w') as f:
# 		f.write(ply_header %dict(vert_num=len(vertices)))
# 		np.savetxt(f,vertices,'%f %f %f %d %d %d')


# output_file = 'pointCloud.ply'

# # Generate point cloud file
# create_point_cloud_file(output_points, output_colors, output_file)
