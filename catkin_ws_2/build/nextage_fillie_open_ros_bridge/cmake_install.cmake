# Install script for directory: /home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/mj/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/mj/catkin_ws/build/nextage_fillie_open_ros_bridge/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/mj/catkin_ws/build/nextage_fillie_open_ros_bridge/catkin_generated/installspace/nextage_fillie_open_ros_bridge.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge/cmake" TYPE FILE FILES
    "/home/mj/catkin_ws/build/nextage_fillie_open_ros_bridge/catkin_generated/installspace/nextage_fillie_open_ros_bridgeConfig.cmake"
    "/home/mj/catkin_ws/build/nextage_fillie_open_ros_bridge/catkin_generated/installspace/nextage_fillie_open_ros_bridgeConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge" TYPE FILE FILES "/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge" TYPE DIRECTORY FILES "/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge" TYPE DIRECTORY FILES "/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge/script" USE_SOURCE_PERMISSIONS)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge" TYPE DIRECTORY FILES "/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge/conf" REGEX "/[^/]*\\.in$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge" TYPE DIRECTORY FILES "/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge/models")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
  message("++ glob files under $ENV{DESTDIR}//home/mj/catkin_ws/install/share/nextage_fillie_open_ros_bridge/conf/")
  file(GLOB _xml_files $ENV{DESTDIR}//home/mj/catkin_ws/install/share/nextage_fillie_open_ros_bridge/conf/*.xml)
  file(GLOB _conf_files $ENV{DESTDIR}//home/mj/catkin_ws/install/share/nextage_fillie_open_ros_bridge/conf/*.conf)
  foreach(_file ${_xml_files} ; ${_conf_files} )
    message("++ sed -i s@/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge@/home/mj/catkin_ws/install/share/nextage_fillie_open_ros_bridge@ ${_file}" )
    message("sed -i s@/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge@/home/mj/catkin_ws/install/share/nextage_fillie_open_ros_bridge@ ${_file}" )
    execute_process(COMMAND sed -i s@/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge@/home/mj/catkin_ws/install/share/nextage_fillie_open_ros_bridge@ ${_file} )
  endforeach()
  
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/nextage_fillie_open_ros_bridge" TYPE DIRECTORY FILES "/home/mj/catkin_ws/src/nextage_fillie_open_ros_bridge/test" USE_SOURCE_PERMISSIONS)
endif()

