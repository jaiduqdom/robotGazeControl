cmake_minimum_required(VERSION 2.8.3)
project(blender_control)

find_package(catkin REQUIRED COMPONENTS
  avatar_msg
  avatar_srv
  roscpp
  rospy
  std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)


