from sympy import Point3D, Line3D
import sys
import os
import paramiko


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
seg_pc_path = "/home/mj/catkin_ws/src/send_pc/segmented_pc.npy"
seg_rgb_path = "/home/mj/catkin_ws/src/send_pc/seg_rgb.npy"
final_send_grasp_command_file_path = "/home/mj/catkin_ws/src/send_pc/select_grasp.txt"
grasp_file_path = "home/mj/catkin_ws/src/receive_grasp/garsp.npy"
final_receive_grasp_command_file_path = "home/mj/catkin_ws/src/receive_grasp/do_grasp.txt"

remote_directory = '/home/munjalu20/receive_pc/'
remote_host = '10.33.24.180'
remote_port = 22
username = 'munjalu20'
key_file = '/home/mj/.ssh/id_rsa'  # Path to your private key file


moving_arm_joint_map = {'larm':'LARM_JOINT5', 
                        'rarm':'RARM_JOINT5'}
def goInit(robot,duration=2):
    robot.setTargetPose('larm', larm_init_position, larm_init_rpy, duration)
    robot.setTargetPose('rarm', rarm_init_position, rarm_init_rpy, duration)
    # robot.setTargetPose('larm', larm_init_position, larm_init_rpy, duration,frame_name="CHEST_JOINT0")
    # robot.setTargetPose('rarm', rarm_init_position, rarm_init_rpy, duration,frame_name="CHEST_JOINT0")
    # robot.setTargetPose('head', head_init_position, head_init_rpy, duration,frame_name="CHEST_JOINT0")
    # robot.setTargetPose('torso', [0, 0, 0], [0, 0, 0], duration)
    robot.waitInterpolation()


def calculate_perpendicular(start_point,end_point,other_point):
    p1,p2,p3 = Point3D(start_point),Point3D(end_point),Point3D(other_point)
    l1 = Line3D(p1, p2)
    l2 = l1.perpendicular_line(p3)
    key_point = l1.intersection(l2)[0]
    return [float(x.evalf()) for x in key_point]



import paramiko
import os

def scp_transfer(local_file, remote_directory, remote_host, remote_port, username, key_file):
    try:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Load the private key
        private_key = paramiko.RSAKey(filename=key_file)
        # print private_key
        # print "hii"
        # Connect to the remote host
        ssh.connect(remote_host, port=remote_port, username=username, pkey=private_key)
        # print "hurr"
        # Initialize SFTP client
        sftp = ssh.open_sftp()
        # print "sftp"
        # Create remote directory if it does not exist

        if not os.path.exists(local_file):
            # print "local file nathi"
            # print(f"Local file {local_file} does not exist.")
            return
        remote_dir = remote_directory
        # print remote_dir
        # print "hmm"
        try:
            sftp.chdir(remote_dir)  # Test if remote path exists
            # print "na"
        except IOError:
            # print "nule"
            sftp.mkdir(remote_dir)  # Create remote directory
            sftp.chdir(remote_dir)
        
        # Transfer the file
        filename = os.path.basename(local_file)
        remote_path = os.path.join(remote_directory, filename)
        # print "befor error"
        sftp.put(local_file, remote_path)
        # print "some error"
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()
        
        # print f"File {local_file} successfully transferred to {remote_host}:{remote_path}"
    except Exception as e:
        print(e)
        # print(f"Error occurred: {e}")

# Variables
# local_file = '/home/mj/file.txt'


# # Transfer the file
# scp_transfer(local_file, remote_directory, remote_host, remote_port, username, key_file)
