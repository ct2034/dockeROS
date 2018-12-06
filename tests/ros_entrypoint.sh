#!/bin/bash
set -e

cd /ws/devel
source "/opt/ros/$ROS_DISTRO/setup.bash"
source "/ws/devel/setup.bash"
echo "$ROS_PACKAGE_PATH"
exec "$@"
