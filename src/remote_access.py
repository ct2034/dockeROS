# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:44:45 2017

@author: Poulastya_Mukherjee
"""

import subprocess
import sys
import remote_access_base
import logging
import yaml
import rospkg

logging.getLogger('root').setLevel(logging.DEBUG)
if logging.getLogger('root').getEffectiveLevel() == logging.DEBUG:
    from debug_print import debug_eval_print
else:
    def debug_eval_print(_):
        pass

usage = "USAGE:\n" + \
        "," * 80 + "\n" \
        "$ rosedge <HOST:PORT> roslaunch ros_naviagtion move_base.launch\n" \
        "Will perform the roslaunch command in a docker container at the mentioned IP\n" + \
        "'" * 80 + "\n" \

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)

try:
    ipwhl = sys.argv[1]
    host = ipwhl.split(':')[0]
    port = ipwhl.split(':')[1]
except:
    print(usage)
    print("Host and/or port not entered! exiting script")
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

print("ROS command to be executed:\n > " + " ".join([roscommand, rospackage, roslaunchfile]))
print("On Server:\n > " + ':'.join([host,port]))

rp = rospkg.RosPack()
fname = rp.get_path('rosedge') + '/config.yaml'
config = yaml.load(open(fname))
dock_obj = remote_access_base.RemoteDock(host, port,
                                         ' '.join([roscommand, rospackage, roslaunchfile]),
                                         config=config,
                                         ca_cert='/home/cch/.docker/ca.pem')
# if not dock_obj.does_exist_on_client():
# else:
#     dock_obj.run_existing_image()


dock_obj.build_docker_image()
dock_obj.run_docker_image()
