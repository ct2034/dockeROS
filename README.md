# ros*edge*
Simply running ros nodes in docker containers on remote robots.

## Idea
This is supposed to deliver tools to use the methods of edge computing for ROS enabled robots.
As of methods we currently mainly focus on a fast and seamless deployment of software to edge devices (i.e. robots, and others).

The **rosedge library** is designed to create and update docker images for ros packages.
There is a CLI to use these capabilities in you development lifecycle and plans to build a GUI that makes use of these tools in a client-server structure.

## Prerequesits
### Server
The python packages required by the server can be installed via `sudo pip install -r requirements.txt`. 
To install docker, you can use [this](https://docs.docker.com/engine/installation/linux/ubuntu/).
You will also need to run a docker registry on your system: `docker run -d -p 5000:5000 --name registry registry`

### Client (Robot)
On the robot you need to have a [docker deamon](https://docs.docker.com/edge/engine/reference/commandline/dockerd/) running with an accesibly API. 
To install docker, you can use [this](https://docs.docker.com/engine/installation/linux/ubuntu/).
A good way to do this on systems running `systemd` is can be found [here](https://www.campalus.com/enable-remote-tcp-connections-to-docker-host-running-ubuntu-15-04/).
We **strongly** recommend to use [TLS for your deamons socket](http://lnr.li/60LYw/)
