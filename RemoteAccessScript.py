# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:44:45 2017

@author: cch-student
"""

import subprocess
import sys
import RefactoredRemoteAccessScript

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout



try:
    ipwhl = sys.argv[1]
    ip = ipwhl.split(':')[0]
    port = ipwhl.split(':')[1]
except:
    print "IP address not entered!exiting script"
    exit()

try:
    roscommand = sys.argv[2]
except:
    print "Ros command not entered!exiting script"
    exit()

try:
    rospackage = sys.argv[3]
except:
    print "Ros package name not entered!exiting script"
    exit()

try:
    roslaunchfile = sys.argv[4]
except:
    print "Ros launch file name not entered!exiting script"
    exit()


dockercmd_img = "docker -H tcp://" + ipwhl + " images"
subprocess.call(dockercmd_img, shell=True)

image = rospackage + "_dockerfile"
dock_obj = RefactoredRemoteAccessScript.RemoteDock(image, ip, port, roscommand, rospackage, roslaunchfile)
var = dock_obj.startcheck()
if (var):
    dock_obj.createDockerImage()
    dock_obj.createDockerContainer()
    dock_obj.runDockerCommands()
    
else:
    dock_obj.runExistingImage()



