#!/usr/bin/env python
#########################################################################################
# @file     nextage_fillie_open_moveit_sample.py(derive from nextage_moveit_sample.py)  #
# @brief    Nextage Move it demo program                                                #
# @date     2015/05/26                                                                  #
# @author   Ryu Yamamoto                                                                #
#########################################################################################
import moveit_commander
import rospy
import geometry_msgs.msg
# import tf2_ros as tf
import tf

def main():
	rospy.init_node("tf_trying")
	robot = moveit_commander.RobotCommander()
	# tfBuffer = tf.Buffer()
	# listener = tf.TransformListener(tfBuffer)
	listener = tf.TransformListener()
	ps = geometry_msgs.msg.PointStamped()
	transformed_point = geometry_msgs.msg.PointStamped()
	print ps.header
	ps.header.frame_id = 'camera'
	print type(ps.point)
	# ps.point.x = 0.060256891844203402
	# input_point =[0.14642932465917435, 0.076750422811173821, 0.66604577336431225]
	input_point = [0.12862738944789368, 0.13724638024449998, 0.72902988516891265]
	ps.point.x = input_point[0]
	# ps.point.y = 0.04742118848306788
	ps.point.y = input_point[1]
	ps.point.z =  input_point[2]

	print ps.point
	rate = rospy.Rate(10.0)
	while not rospy.is_shutdown():
		try:
			# print listener.getFrames()
			trans =      listener.lookupTransform('WAIST', 'camera', rospy.Time())
			transformed_point=listener.transformPoint('WAIST',ps)
			print transformed_point.header
			print [transformed_point.point.x ,transformed_point.point.y,transformed_point.point.z]
			# trans = tfBuffer.lookup_transform('WAIST', 'camera', rospy.Time())
			# print tfBuffer.getFrames()
			# print listener.
			# print trans

		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			rate.sleep()
			continue
	# trans = tfBuffer.lookup_transform('WAIST', '/RARM_LINK5', rospy.Time())
	
	# tl = tf.TransformListener()
	# print tl.getFrameStrings()
	# t = tf.Transformer(True, rospy.Duration(10.0))

	# print t.getFrameStrings()
	
	# print tf.TransformListener().lookupTransform('/WAIST', '/LARM_JOINT', rospy.Time(0))
	# print "=" * 10, " Robot Groups:"
	# print robot.get_group_names()

	# print "=" * 10, " Printing robot state"
	# print robot.get_current_state()
	# print "=" * 10 

	# rarm = moveit_commander.MoveGroupCommander("right_arm")
	# larm = moveit_commander.MoveGroupCommander("left_arm")

	# print "=" * 15, " Right arm ", "=" * 15
	# print "=" * 10, " Reference frame: %s" % rarm.get_planning_frame()
	# print "=" * 10, " Reference frame: %s" % rarm.get_end_effector_link()
    
	# print "=" * 15, " Left ight arm ", "=" * 15
	# print "=" * 10, " Reference frame: %s" % larm.get_planning_frame()
	# print "=" * 10, " Reference frame: %s" % larm.get_end_effector_link()

	# #Right Arm Initial Pose
	# rarm_initial_pose = rarm.get_current_pose().pose
	# print "=" * 10, " Printing Right Hand initial pose: "
	# print rarm_initial_pose

	# #Light Arm Initial Pose
	# larm_initial_pose = larm.get_current_pose().pose
	# larm_camera_pose = larm.get_current_pose().pose
	# print larm_camera_pose 
	# print "=" * 10, " Printing Left Hand initial pose: "
	# print larm_initial_pose

	# target_pose_r = geometry_msgs.msg.Pose()
	# target_pose_r.position.x = 0.3
	# target_pose_r.position.y = -0.3
	# target_pose_r.position.z = 0.1
	# target_pose_r.orientation.x = 0
	# target_pose_r.orientation.y = 0
	# target_pose_r.orientation.z = 0
	# target_pose_r.orientation.w = 1
	# rarm.set_pose_target(target_pose_r)
	# #0.0012257975662421049, 0.10202348706736851, 0.76334241020057336
	# print "=" * 10," plan1 ..."
	# rarm.go()
	# rospy.sleep(1)
	
	# target_pose_l = [
	# 	target_pose_r.position.x,
	# 	-target_pose_r.position.y,
	# 	target_pose_r.position.z,
	# 	target_pose_r.orientation.x,
	# 	target_pose_r.orientation.y,
	# 	target_pose_r.orientation.z,
	# 	target_pose_r.orientation.w
	# ]
	# larm.set_pose_target(target_pose_l)

	# print "=" * 10," plan2 ..."
	# larm.go()
	# rospy.sleep(1)
	
	# #Clear pose
	# rarm.clear_pose_targets()

	# #Right Hand
	# target_pose_r.position.x = 0.2
	# target_pose_r.position.y = 0
	# target_pose_r.position.z = 0.3
	# target_pose_r.orientation.x = 0
	# target_pose_r.orientation.y = 0
	# target_pose_r.orientation.z = 0
	# target_pose_r.orientation.w = 1
	# rarm.set_pose_target(target_pose_r)
	
	# print "=" * 10, " plan3..."
	# rarm.go()
	# rospy.sleep(1)

	# print "=" * 10,"Initial pose ..."
	# rarm.set_pose_target(rarm_initial_pose)
	# larm.set_pose_target(larm_initial_pose)
	# rarm.go()
	# larm.go()
	rospy.sleep(2)
	
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
