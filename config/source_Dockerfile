FROM ros:kinetic-robot
# connect to host via bridge
ENV ROS_MASTER_URI=http://172.17.0.1:11311

RUN apt-get update
RUN apt-get install -y\
 ros-kinetic-navigation 

SHELL ["bash", "-c"]
RUN mkdir -p /ws/src/$PACKAGE
COPY . /ws/src/$PACKAGE
RUN source /opt/ros/kinetic/setup.bash;\
 cd /ws/src;\
 catkin_init_workspace;\
 cd /ws;\
 catkin_make

# adding some things
RUN echo "#!/bin/bash" | tee /ros_entrypoint.sh;\
 echo "set -e" >> /ros_entrypoint.sh;\
 echo "source /ws/devel/setup.bash" >> /ros_entrypoint.sh;\
 echo "export ROS_IP=\$(hostname -I)" >> /ros_entrypoint.sh;\
 echo "roslaunch $PACKAGE navigation.launch" >> /ros_entrypoint.sh

RUN cat /ros_entrypoint.sh
