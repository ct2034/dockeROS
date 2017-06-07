# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:32:49 2017

@author: cch-student
"""

import docker

def createDockerContainer(image, ip,port, rospackage):
    ip_str = "tcp://" + ip + ":" + port
    cli = docker.Client(base_url=ip_str)
    container = cli.create_container(image,
                                     hostname='3e93a4b05cf6',
                                     user='1000:1000',
                                     stdin_open=True,
                                     tty=True,
                                     entrypoint='/ros_entrypoint.sh',
                                     command=["bash"],
                                     environment=[
                                         "PATH/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
                                     working_dir='/',
                                     volumes='$HOME/.config/catkin:/.config/catkin:ro')
    cli.start(container['Id'])
    #return container['Id']
    var = len(container['Id'])
    return var == 64
    
def test_answer():
    assert createDockerContainer("teleop_twist_keyboard_dockerfile", '10.2.1.11','1139','teleop_twist_keyboard') == True
