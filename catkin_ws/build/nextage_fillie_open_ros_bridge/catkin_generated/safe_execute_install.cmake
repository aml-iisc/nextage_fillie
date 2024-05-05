execute_process(COMMAND "/home/mj/catkin_ws/build/nextage_fillie_open_ros_bridge/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/mj/catkin_ws/build/nextage_fillie_open_ros_bridge/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
