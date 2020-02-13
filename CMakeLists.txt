cmake_minimum_required(VERSION 2.8.3)
project(ur5_photo_creator)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_package()

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
catkin_install_python(
	PROGRAMS
	    scripts/photo_node.py
      scripts/photo_creator.py
	DESTINATION
	    ${CATKIN_PACKAGE_BIN_DESTINATION}
)
