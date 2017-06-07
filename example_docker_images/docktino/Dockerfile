FROM ros:kinetic-robot

# install ros-kinetic-navigation
RUN apt-get update && \
    apt-get -y install sudo && \
    useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo && \
    apt-get install -y git && \ 
    apt-get update && \
    apt-get install -y \
    ros-kinetic-navigation \
    ros-kinetic-roslint \
    ros-kinetic-image* \
    ros-kinetic-teleop-twist-keyboard \
    ros-kinetic-gmapping && \
   # apt-get update && \
    apt-get install wget -y && \ 
    wget -qO - http://packages.openrobotino.org/keyFile | apt-key add - && \
    sudo su && \
    echo "deb http://packages.openrobotino.org/xenial xenial main" > /etc/apt/sources.list.d/openrobotino.list && \
    apt-get update && \
    apt-get install lighttpd && \
    apt-get update && \
    apt-get install rec-rpc robotino-common robotino-daemons robotino-api2 robotino3-firmware -y  && \
    # clean-up
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

