FROM ros:kinetic-robot

#ros-kinetic-navigation
RUN apt-get update && \
	apt-get install -y \ 
	ros-kinetic-navigation \ 
	ros-kinetic-roslint \ 
	ros-kinetic-image* 


# Create user
RUN useradd -ms /bin/bash ros && \
    adduser ros sudo && \
    adduser root sudo && \
    echo "%sudo   ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ros

EXPOSE 22 80

COPY ./ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["source"]

