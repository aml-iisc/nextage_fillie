larm_init_position= [0.32, 0.16529070140431193, 0.18671804615844229]
larm_init_rpy=[0, 0, 0]
rarm_init_position= [0.32, -0.16529070140431207, 0.18671804615844234]
rarm_init_rpy=[0, -0, 0]

def goInit():
    robot.setTargetPose('larm', larm_init_position, larm_init_rpy, 4)
    robot.setTargetPose('rarm', rarm_init_position, rarm_init_rpy, 4)
    robot.waitInterpolation()
    