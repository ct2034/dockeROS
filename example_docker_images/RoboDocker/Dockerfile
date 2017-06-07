FROM ros:kinetic-robot

# install ros-kinetic-navigation
RUN apt-get update && \
    apt-get install -y \
    ros-kinetic-navigation \
    ros-kinetic-roslint \
    ros-kinetic-image* \
    ros-kinetic-teleop-twist-keyboard \
    ros-kinetic-gmapping && \

    # clean-up
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
