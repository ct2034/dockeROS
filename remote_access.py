# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:44:45 2017

@author: Poulastya_Mukherjee
"""

import subprocess
import sys
import remote_access_base

usage = "USAGE:\n" + \
        "," * 80 + "\n" \
        "$ rosedge <IP> roslaunch ros_naviagtion move_base.launch\n" \
        "Will perform the roslaunch command in a docker container at the mentioned IP\n" + \
        "'" * 80 + "\n" \

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)

try:
    ipwhl = sys.argv[1]
    ip = ipwhl.split(':')[0]
    port = ipwhl.split(':')[1]
except:
    print(usage)
    print("IP address not entered! exiting script")
    exit()

try:
    roscommand = sys.argv[2]
except:
    print(usage)
    print("Ros command not entered! exiting script")
    exit()

try:
    rospackage = sys.argv[3]
except:
    print(usage)
    print("Ros package name not entered! exiting script")
    exit()

try:
    roslaunchfile = sys.argv[4]
except:
    print(usage)
    print("Ros launch file name not entered! exiting script")
    exit()

dockercmd_img = "docker -H tcp://" + ipwhl + " images"
subprocess.call(dockercmd_img, shell=True)

image = rospackage + "_dockerfile"
dock_obj = remote_access_base.RemoteDock(image, ip, port, roscommand, rospackage, roslaunchfile)
var = dock_obj.startcheck()
if var:
    dock_obj.create_docker_image()
    dock_obj.create_docker_container()
    dock_obj.run_docker_commands()
    
else:
    dock_obj.run_existing_image()



