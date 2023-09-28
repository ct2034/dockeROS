| :warning: UNMAINTAINED |
|:----------------------:|

Sorry, this is no longer maintained.
But there are many __great__ alternatives:
- [rocker](https://github.com/osrf/rocker)
- [docker-ros](https://github.com/ika-rwth-aachen/docker-ros)
- [useful-defaults](https://discourse.ros.org/t/announcing-docker-run-docker-run-and-docker-exec-with-useful-defaults-for-robotics/32680)

# docke*ROS*

Simply running ROS nodes in docker containers on robots.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/ct2034/dockeROS/compare)
t: [![tavis_status](https://travis-ci.org/ct2034/dockeROS.svg?branch=master)](https://travis-ci.org/ct2034/dockeROS)
bf: [![Build Status](http://build.ros.org/job/Kdev__dockeros__ubuntu_xenial_amd64/badge/icon)](http://build.ros.org/job/Kdev__dockeros__ubuntu_xenial_amd64/)
bf_doc: [![Build Status](http://build.ros.org/buildStatus/icon?job=Kdoc__dockeros__ubuntu_xenial_amd64)](http://build.ros.org/job/Kdoc__dockeros__ubuntu_xenial_amd64/)
cc: [![Maintainability](https://api.codeclimate.com/v1/badges/23f9444fa2a2a1dc3d8c/maintainability)](https://codeclimate.com/github/ct2034/dockeROS/maintainability)

## Idea

This is supposed to deliver tools to use the methods of **edge computing** for ROS enabled robots.
These methods include fast and seamless deployment of software to edge devices (i.e. robots, and others).

The **dockeros library** is designed to create and update docker images for ros packages.
There is a CLI to use these capabilities in your development lifecycle that makes use of these tools in a client-server structure.

## Media

### Video

[![video](https://img.youtube.com/vi/Ubdc96GkO3M/1.jpg)](https://www.youtube.com/watch?v=Ubdc96GkO3M)

*Presentation at ROS Industrial Conference 2018*

### Podcast

[![podcast](https://assets.libsyn.com/secure/content/29282579/?height=90&width=90)](https://www.theconstructsim.com/rdp-034-docker-ros-dockeros-christian-henkel/)

*Podcast with Ricardo Tellez*

## Prerequesits

### On your PC (the Server)

The python packages required by the server can be installed via `pip install -r requirements.txt`.
To install docker, you can use [this](https://docs.docker.com/engine/installation/linux/ubuntu/).

#### Optional: Registry

Without a registry, you will need to build the images on the robot they should run on.
If you want to build them in a central place (the server), you need to run a docker registry on that server: `docker run -d -p 5000:5000 --name registry registry`. 
You can also use the `unsafe_registry` in this repository. 
It will allow CORS (which is why it is called unsafe).

### On the Robot (Client)

On the robot you need to have a [docker deamon](https://docs.docker.com/edge/engine/reference/commandline/dockerd/) running with an accesible API.
To install docker, you can use [this](https://docs.docker.com/engine/installation/linux/ubuntu/).
A good way to do this on systems running `systemd` is can be found [here](https://www.campalus.com/enable-remote-tcp-connections-to-docker-host-running-ubuntu-15-04/).
We **strongly** recommend to use [TLS for your deamons socket](http://lnr.li/60LYw/)

## The CLI

```
usage: dockeros [-h] [-e | -i HOST:PORT] [-f DOCKERFILE] [-n]
                {build,run,stop,push} ...

Simply running ros nodes in docker containers on remote robots.

positional arguments:
  {build,run,stop,push}
                        build: Creates an image that can run roscommand
                        run: Runs an image with your_roscommand (and builds it first)
                        stop: Stops image that runs that command
                        push: Push image to predefined registry
  roscommand            Everything after the subcommand will be interpreted as the ros command to be run in your image

optional arguments:
  -h, --help            show this help message and exit
  -e, --env             use the existing docker environment (see https://dockr.ly/2zMPc17 for details)
  -i HOST:PORT, --ip HOST:PORT, --host HOST:PORT
                        set the host (robot) to deploy image to
  -f DOCKERFILE, --dockerfile DOCKERFILE
                        use a custom Dockerfile
  -n, --no-build        dont (re-)build the image before running
```

![screencast of dockeros run](https://github.com/ct2034/dockeROS/blob/master/doc/dockeros_run.gif)

## Contribution
All contributions are welcome. Especially important is at the moment:
### Testing
Please open issues for all problems you encounter. 
Please make sure, that your problem is reproducible though: Add the rosdistro, package, exact command and Dockerfile (if applicable) that you are using

## Troubleshooting
### Registry with http
When you get this error: `{"errorDetail":{"message":"Get https://YOUR_REGISTRY:5000/v2/: http: server gave HTTP response to HTTPS client"},"error":"Get https://YOUR_REGISTRY:5000/v2/: http: server gave HTTP response to HTTPS client"}` while trying to push:

Add the server to your unsafe registries in `daemon.json` (default at `/etc/docker/daemon.json` )
```
"insecure-registries":["YOUR_REGISTRY:5000"]
```
and restart your docker deamon.
```
sudo systemctl restart docker
```
[source](https://stackoverflow.com/questions/49674004/docker-repository-server-gave-http-response-to-https-client#49675214)
