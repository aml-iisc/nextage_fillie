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

errormsg_noros = 'No ROS Master found. Without it, you cannot use ROS from' \
                 ' this script, but can use RTM. To use ROS, do not forget' \
                 ' to run rosbridge. How to do so? --> http://wiki.ros.org/rtmros_nextage/Tutorials/Operating%20Hiro%2C%20NEXTAGE%20OPEN'
# print errormsg_noros
# print "hii"
# (-0.012634121524210484, -0.062091464383531039, 0.97242709522386672)
larm_init_position= [0.32, 0.16529070140431193, 0.18671804615844229]
larm_init_rpy=[0, 0, 0]
rarm_init_position= [0.32, -0.16529070140431207, 0.18671804615844234]
rarm_init_rpy=[0, -0, 0]

def calculate_perpen(start_point,end_point,other_point):
    # print(start_point,end_point,other_point)
    p1,p2,p3 = Point3D(start_point),Point3D(end_point),Point3D(other_point)
    l1 = Line3D(p1, p2)
    l2 = l1.perpendicular_line(p3)
    # isPerpendicular =l1.is_perpendicular(l2)
    # print(isPerpendicular)
    key_point = l1.intersection(l2)[0]
    # print(key_point)
    # print(key_point.evalf())
    # print([x.evalf() for x in key_point])
    # print(l1.contains(key_point))
    return [float(x.evalf()) for x in key_point]

def goInit():
    robot.setTargetPose('larm', larm_init_position, larm_init_rpy, 2)
    robot.setTargetPose('rarm', rarm_init_position, rarm_init_rpy, 2)
    robot.waitInterpolation()
    
    # robot.waitInterpolation()

def func():
    listener = tf.TransformListener()
    while not rospy.is_shutdown():
        camera_ps = geometry_msgs.msg.PointStamped()
        waist_transformed_point = geometry_msgs.msg.PointStamped()
        LS_transformed_point = geometry_msgs.msg.PointStamped()
        RS_transformed_point= geometry_msgs.msg.PointStamped()
        print camera_ps.header
        camera_ps.header.frame_id = 'camera'
        print type(camera_ps.point)
        string_input_point = raw_input("Please enter the point in the camera frame in the x,y,z format: ")
        list_s_input = string_input_point.split(",")
        chekcing_list = [float(num) for num in list_s_input]
        print chekcing_list 
        input_point = [0.12862738944789368, 0.13724638024449998, 0.72902988516891265] # in camera frame
        input_point = chekcing_list
        camera_ps.point.x = input_point[0]
        camera_ps.point.y = input_point[1]
        camera_ps.point.z = input_point[2]
        print camera_ps.point
        # confirmation = raw_input("Please type YES to move the robot: ")
        # print confirmation
        yes = 'YES'
        # if confirmation == yes:
        if True:
            print "hii"
            rate = rospy.Rate(10.0)
            try:
                waist_trans = listener.lookupTransform('WAIST', 'camera', rospy.Time())
                ls_trans = listener.lookupTransform('WAIST','LS',rospy.Time())
                print ls_trans
                rs_trans = listener.lookupTransform('WAIST','RS',rospy.Time())
                print rs_trans
                waist_transformed_point = listener.transformPoint('WAIST',camera_ps)
                LS_transformed_point = listener.transformPoint('LS',camera_ps)
                RS_transformed_point = listener.transformPoint('RS',camera_ps)
                # all_wanted_transformation = [waist_transformed_point,LS_transformed_point,RS_transformed_point]
                print waist_transformed_point.header.frame_id,LS_transformed_point.header.frame_id,RS_transformed_point.header.frame_id
                print [waist_transformed_point.point.x ,waist_transformed_point.point.y,waist_transformed_point.point.z]
                print [LS_transformed_point.point.x ,LS_transformed_point.point.y,LS_transformed_point.point.z]
                print [RS_transformed_point.point.x ,RS_transformed_point.point.y,RS_transformed_point.point.z]
                (moving_arm,start_point) = ("larm",ls_trans[0]) if waist_transformed_point.point.y>0 else ("rarm",rs_trans[0])
                # moving_arm = "larm" if waist_transformed_point.point.y>0 else "rarm"
                if moving_arm == 'larm':
                    moving_joint = 'LARM_JOINT5'
                elif moving_arm == 'rarm':
                    moving_joint = 'RARM_JOINT5'    
                # start_point = robot.getCurrentPosition(moving_joint)
                end_point = [waist_transformed_point.point.x ,waist_transformed_point.point.y,waist_transformed_point.point.z]
                direction = [a - b for a, b in zip(end_point, start_point)]
                start_point = calculate_perpen(start_point,end_point,robot.getCurrentPosition(moving_joint))
                direction = [a - b for a, b in zip(end_point, start_point)]
                for i in np.arange(0,1,0.02):
                    pos = [a + b*i for a,b in zip(start_point,direction)]
                    # print i
                print moving_arm
                # select_transformation = 0

                
                joint_pos = robot.getCurrentPosition(moving_joint)
                joint_rpy = robot.getCurrentRPY(moving_joint)
                duration = 2
                for i in np.arange(0,1,0.01):
                    joint_pos = [a + b*i for a,b in zip(start_point,direction)]
                    robot.setTargetPose(moving_arm, joint_pos, joint_rpy, duration)
                    robot.waitInterpolation()
                    duration = 0.1
                print("reached the farthest point it can reach")
                time.sleep(3)
                goInit()
                # robot.goInitial()
                # print(robot.getCurrentRPY('LARM_JOINT5'))
                # print(robot.getCurrentRPY('RARM_JOINT5'))

            
			# trans = tfBuffer.lookup_transform('WAIST', 'camera', rospy.Time())
			# print tfBuffer.getFrames()
			# print listener.
			# print trans

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rate.sleep()
                continue
        else:
            print "noo"


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

    if args.dio_ver:
        robot.set_hand_version(args.dio_ver)

    try:
        ros = ROS_Client()
        func()
        # rospy.init_node("tf_trying")
        # robot.goInitial()
    except rospy.ROSInitException as e:
        print('[nextage_fillie_open.py] {}'.format(e))
    except socket.error as e: 
        print("\033[31m%s\n%s\033[0m" % (e.strerror, errormsg_noros))