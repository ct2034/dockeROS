cmake_minimum_required(VERSION 2.8.3)
project(dockeros)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_add_env_hooks(dockeROS SHELLS bash DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)

#############
## Install ##
#############

catkin_python_setup()

catkin_install_python(PROGRAMS src/dockeros/cli.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

if(CATKIN_ENABLE_TESTING)
 find_package(rostest REQUIRED)
 add_rostest(tests/image.test)
endif()
