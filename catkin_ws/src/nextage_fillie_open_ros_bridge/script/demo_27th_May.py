from general_support import *
import socket
from hironx_ros_bridge.ros_client import ROS_Client
from nextage_fillie_open_ros_bridge import nextage_fillie_open_client
import rospy
from hrpsys import rtm
import argparse
import geometry_msgs.msg
import tf
import numpy as np
import time
from sympy import Point3D, Line3D
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import os
import struct
import ros_numpy
import math
import signal



errormsg_noros = 'No ROS Master found. Without it, you cannot use ROS from' \
                 ' this script, but can use RTM. To use ROS, do not forget' \
                 ' to run rosbridge. How to do so? --> http://wiki.ros.org/rtmros_nextage/Tutorials/Operating%20Hiro%2C%20NEXTAGE%20OPEN'

#default


def point_cloud_callack(point_cloud_msg):
    global point_cloud_data
    try:
        point_cloud_data = np.frombuffer(point_cloud_msg.data, dtype=np.uint8)
    except:
        print("Point cloud is not proper")

def image_callback_left(img_msg):
    global left_image
    # Try to convert the ROS Image message to a CV2 Image
    try:
        left_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

def object_centre_point(segmented_image,raw_point_cloud_matrix):
    x=0
    y=0
    z=0
    count=0
    camera_ps = geometry_msgs.msg.PointStamped()
    camera_ps.header.frame_id = 'camera'
    for i in range(1096):
        for j in range(1936):
            # print(segmented_image[i][j])
            # math.isnan(x)
            if segmented_image[i][j]>0 and (not math.isnan(raw_point_cloud_matrix[i][j][0])) and (not math.isnan(raw_point_cloud_matrix[i][j][1])) and (not math.isnan(raw_point_cloud_matrix[i][j][2])):
                x = x + raw_point_cloud_matrix[i][j][0]
                y = y + raw_point_cloud_matrix[i][j][1]
                z = z + raw_point_cloud_matrix[i][j][2]
                count = count+1
    camera_ps.point.x = x/count
    camera_ps.point.y = y/count
    camera_ps.point.z = z/count

    return camera_ps

def look_at_this_point(camera_point,transform_listener):
    
    waist_transformed_point = geometry_msgs.msg.PointStamped()
    rate = rospy.Rate(10.0)
    try:
        waist_trans = transform_listener.lookupTransform('WAIST', 'camera', rospy.Time())
        # print(waist_trans)
        waist_transformed_point = transform_listener.transformPoint('WAIST',camera_point)
        ls_trans = transform_listener.lookupTransform('WAIST','LS',rospy.Time())
        rs_trans = transform_listener.lookupTransform('WAIST','RS',rospy.Time())
        (l_moving_arm,l_start_point) = ("larm",ls_trans[0]) if waist_transformed_point.point.y>0 else ("rarm",rs_trans[0])
        l_moving_joint = moving_arm_joint_map[l_moving_arm]
        l_end_point = [waist_transformed_point.point.x ,waist_transformed_point.point.y,waist_transformed_point.point.z]
        l_start_point = calculate_perpendicular(l_start_point,l_end_point,robot.getCurrentPosition(l_moving_joint))
        l_direction = [a - b for a, b in zip(l_end_point, l_start_point)]
        return True,l_start_point,l_direction,l_moving_arm,l_moving_joint
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("Something wrong with transformations!!!")
        rate.sleep()
        return False,0,0,0,0

def move_the_robot(start_point,direction,moving_arm,moving_joint,fining=0.01,duration=0.1):
    joint_pos = robot.getCurrentPosition(moving_joint)
    joint_rpy = robot.getCurrentRPY(moving_joint)
    in_duration = 2
    for i in np.arange(0,1,fining):
        joint_pos = [a + b*i for a,b in zip(start_point,direction)]
        robot.setTargetPose(moving_arm, joint_pos, joint_rpy, in_duration)
        robot.waitInterpolation()
        in_duration = duration
    print("Reached the farthest point it can reach...")

def save_image_and_prompt(prompt):
    global left_image
    cv2.imwrite(image_file_path,left_image)
    local_left_image_resized = cv2.resize(left_image, (width, 480))
    cv2.startWindowThread()
    cv2.namedWindow('Saved Image')
    cv2.imshow('Saved Image',local_left_image_resized)
    prompt_file = open(prompt_file_path,"w")
    L = [prompt]
    prompt_file.writelines(L)
    prompt_file.close()

    temp_file = open(final_send_command_file_path,"w")
    temp_file.close()
    print("files are saved")

def wait_and_return_segmented_image():
    while not (os.path.exists(segmented_image_path) and os.path.exists(final_receive_command_file_path)):
        pass
    local_segmented_image = cv2.imread(segmented_image_path,0)
    # print(segmented_image.shape)
    local_segmented_image_resized = cv2.resize(local_segmented_image, (width, 480))
    # final_xyz[se]
    # print(final_xyz.shape)
    print(local_segmented_image_resized.shape)
    cv2.namedWindow('Resized segmented_image')
    cv2.imshow('Resized segmented_image',local_segmented_image_resized)
    os.remove(final_receive_command_file_path)
    os.remove(segmented_image_path)
    return local_segmented_image

def evaluate_point_cloud():
    global point_cloud_data
    local_point_cloud = point_cloud_data.reshape((1096,1936,32))
    local_point_cloud = local_point_cloud.view(np.float32)
    # print(data_array.shape)
    x = local_point_cloud[:, :, 0]
    y = local_point_cloud[:, :, 1]
    z = local_point_cloud[:, :, 2]
    # extra_floats1 = data_array[:, :, 3*float_size:].astype(dtype=np.float32).reshape((image_height, image_width, 8 - 3))
    final_matrix = np.stack((x, y, z), axis=-1)
    # print(final_matrix.shape)
    return final_matrix




def constant_prompt_and_point():
    transform_listener = tf.TransformListener()
    while not rospy.is_shutdown():
        try:
            prompt = raw_input("Tell me what to point at: ")
        except KeyboardInterrupt:
            sys.exit(0)
        save_image_and_prompt(prompt)
        raw_point_cloud_matrix = evaluate_point_cloud()
        segmented_image = wait_and_return_segmented_image()
        camera_point = object_centre_point(segmented_image,raw_point_cloud_matrix)
        tf_success,start_point,direction,moving_arm,moving_joint = look_at_this_point(camera_point,transform_listener)
        if tf_success:
            confirmation = raw_input("Please type YES to move the robot(Caution: Robot will move!!!!): ")
            yes = 'YES'
            if confirmation == yes:
                move_the_robot(start_point,direction,moving_arm,moving_joint)
                time.sleep(3)
                goInit(robot,4)
            else:
                print("Not moving the robot, Okay!!!")
        else:
            print("Transform listener not working fine")
        cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hiro command line interpreters')
    parser.add_argument('--host', help='corba name server hostname')
    parser.add_argument('--port', help='corba name server port number')
    parser.add_argument('--modelfile', help='robot model file nmae')
    parser.add_argument('--robot', help='robot modlule name (RobotHardware0 for real robot, Robot()')
    parser.add_argument('--dio_ver', help="Version of digital I/O. Only users "
                        "whose robot was shipped before Aug 2014 need to "
                        "define this, and the value should be '0.4.2'.")
    args, unknown = parser.parse_known_args()

    if args.host:
        rtm.nshost = args.host
    if args.port:
        rtm.nsport = args.port
    if not args.robot:
        args.robot = "RobotHardware0" if args.host else "HiroNX(Robot)0"
    if not args.modelfile:
        args.modelfile = "/opt/jsk/etc/FILLIE/model/main.wrl" if args.host else "" 
    # print("hii")
    # support old style format
    if len(unknown) >= 2:
        args.robot = unknown[0]
        args.modelfile = unknown[1]
    robot = nxc = nextage_fillie_open_client.NextageFillieOpenClient()
    # Use generic name for the robot instance. This enables users on the
    # script commandline (eg. ipython) to run the same commands without asking
    # them to specifically tell what robot they're using (eg. hiro, nxc).
    # This is backward compatible so that users can still keep using `nxc`.
    # See http://code.google.com/p/rtm-ros-robotics/source/detail?r=6926
    robot.init(robotname=args.robot, url=args.modelfile)

    bridge = CvBridge()
    left_image  = 0
    point_cloud_data = 0
    flag = 0
    # global final_xyz
    signal.signal(signal.SIGINT,shutup)
    if args.dio_ver:
        robot.set_hand_version(args.dio_ver)

    try:
        hironx_ros = ROS_Client()

        # rospy.init_node('prompt_and_point', anonymous=True)
        rospy.loginfo("Hello ROS! Welcome to prompt and point!!")

        image_sub = rospy.Subscriber("/left/image_rect_color", Image, image_callback_left)
        pointcloud_sub = rospy.Subscriber("/points2", PointCloud2, point_cloud_callack)

        constant_prompt_and_point()
        # rospy.init_node("tf_trying")
        # robot.goInitial()
    except KeyboardInterrupt:
        sys.exit(0)
    except rospy.ROSInitException as e:
        print('[nextage_fillie_open.py] {}'.format(e))
    except socket.error as e: 
        print("\033[31m%s\n%s\033[0m" % (e.strerror, errormsg_noros))