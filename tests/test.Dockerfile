FROM ros:kinetic

RUN apt update
RUN apt install -y python-pip python-catkin-tools

COPY requirements.txt .
RUN pip install -r requirements.txt

# ros workspace
RUN mkdir -p /ws/src/dockeROS
COPY . /ws/src/dockeROS
WORKDIR /ws/src
RUN /ros_entrypoint.sh catkin_init_workspace
WORKDIR /ws
RUN /ros_entrypoint.sh catkin build
COPY ./config/ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh
