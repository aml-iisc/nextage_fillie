from sympy import Point3D, Line3D
import sys

larm_init_position= [0.32, 0.16529070140431193, 0.18671804615844229]
larm_init_rpy=[0, 0, 0]
rarm_init_position= [0.32, -0.16529070140431207, 0.18671804615844234]
rarm_init_rpy=[0, 0, 0]
head_init_position = [0.0, 0.0, 0.705]
head_init_rpy = [0, 0, 0]
ratio = float(1936.0)/1096.0
width = int(480*ratio)

prompt_file_path= "/home/mj/catkin_ws/src/send/this_is_the_prompt.txt"
image_file_path= "/home/mj/catkin_ws/src/send/please_segment_me.png"
final_send_command_file_path = "/home/mj/catkin_ws/src/send/do_segment.txt"
segmented_image_path = "/home/mj/catkin_ws/src/receive/segmented.png"
final_receive_command_file_path = "/home/mj/catkin_ws/src/receive/segmentation_done.txt"

moving_arm_joint_map = {'larm':'LARM_JOINT5', 
                        'rarm':'RARM_JOINT5'}
def goInit(robot,duration=2):
    robot.setTargetPose('larm', larm_init_position, larm_init_rpy, duration,frame_name="CHEST_JOINT0")
    robot.setTargetPose('rarm', rarm_init_position, rarm_init_rpy, duration,frame_name="CHEST_JOINT0")
    # robot.setTargetPose('head', head_init_position, head_init_rpy, duration,frame_name="CHEST_JOINT0")
    # robot.setTargetPose('torso', [0, 0, 0], [0, 0, 0], duration)
    robot.waitInterpolation()


def calculate_perpendicular(start_point,end_point,other_point):
    p1,p2,p3 = Point3D(start_point),Point3D(end_point),Point3D(other_point)
    l1 = Line3D(p1, p2)
    l2 = l1.perpendicular_line(p3)
    key_point = l1.intersection(l2)[0]
    return [float(x.evalf()) for x in key_point]

def shutup(sig,frame):
    robot.servoOff()
    sys.exit(0)