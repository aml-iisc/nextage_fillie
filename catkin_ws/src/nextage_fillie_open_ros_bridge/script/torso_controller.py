import socket

from hironx_ros_bridge.ros_client import ROS_Client
# This should come earlier than later import.
# See http://code.google.com/p/rtm-ros-robotics/source/detail?r=6773
from nextage_fillie_open_ros_bridge import nextage_fillie_open_client
import rospy
from hrpsys import rtm
import argparse
import keyboard
import signal
from curtsies import Input 
import sys
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2

errormsg_noros = 'No ROS Master found. Without it, you cannot use ROS from' \
                 ' this script, but can use RTM. To use ROS, do not forget' \
                 ' to run rosbridge. How to do so? --> http://wiki.ros.org/rtmros_nextage/Tutorials/Operating%20Hiro%2C%20NEXTAGE%20OPEN'

ratio = float(1936.0)/1096.0
width = int(480*ratio)

def shutup(sig,frames):
    cv2.destroyAllWindows()
    robot.goInitial()
    robot.servoOff()
    # cv2.destroyAllWindows()
    sys.exit(0)
    # exit(0)

def image_callback_left(img_msg):
    global rect_left_image
    # log some info about the image topic
    # rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        rect_left_image = bridge.imgmsg_to_cv2(img_msg, "bgr8")
        rect_left_image_resized = cv2.resize(rect_left_image, (width, 480))
        cv2.startWindowThread()
        cv2.namedWindow('Live Image')
        cv2.imshow('Live Image',rect_left_image_resized)
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

def torso_controller(robot,fining=0.05):
    robot.servoOn()
    pos = robot.getCurrentPosition("CHEST_JOINT0")
    rpy = robot.getCurrentRPY("CHEST_JOINT0")
    print(pos,rpy)
    (a,b,c)= rpy
    while not rospy.is_shutdown():
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                # print(type(e))
                if (e==unicode("KEY_LEFT")):
                    c = c + fining
                elif(e==unicode("KEY_RIGHT")):
                    c = c - fining
                rpy = (a,b,c)
                robot.setTargetPose("torso",pos,rpy,1)
                robot.waitInterpolation()
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hiro command line interpreters')
    # parser.add_argument('--show_image',help='show image or not')
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
    rect_left_image  = 0
    # global final_xyz
    signal.signal(signal.SIGINT,shutup)
    if args.dio_ver:
        robot.set_hand_version(args.dio_ver)

    try:
        hironx_ros = ROS_Client()

        # # rospy.init_node('prompt_and_point', anonymous=True)
        # rospy.loginfo("Hello ROS! Welcome to prompt and point!!")
        # if args.show_image == "1":
        image_sub = rospy.Subscriber("/left/image_rect_color", Image, image_callback_left)
        # pointcloud_sub = rospy.Subscriber("/points2", PointCloud2, point_cloud_callack)
        torso_controller(robot)
        # rospy.init_node("tf_trying")
        # robot.goInitial()
    except KeyboardInterrupt:
        sys.exit(0)
    except rospy.ROSInitException as e:
        print('[nextage_fillie_open.py] {}'.format(e))
    except socket.error as e: 
        print("\033[31m%s\n%s\033[0m" % (e.strerror, errormsg_noros))