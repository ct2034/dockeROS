#!/bin/bash
# My first script
ip=$1
node=$2
if [[ -n "$ip" ]]; then
	docker -H tcp://$ip:2375 images;
	echo -n "enter docker image name";
	read image;
	docker -H tcp://$ip:2375 run -it --rm -u "$(id -u):$(id -g)" -v $HOME/.ros:/.ros -v $HOME/.config/catkin:/.config/catkin:ro -v $(pwd):$(pwd) -w $(pwd) $image
	if [[ $? -ne 0 ]]; then
		echo -n "wrong image name!!!" -n
	fi
else 
	echo "IP ADDRESS MISSING!!!!"
fi
