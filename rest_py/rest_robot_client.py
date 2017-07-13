# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:32:30 2017

@author: cch-student
"""
import falcon
import json
import socket
from uuid import getnode as get_mac
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
doc = {'ip_add':s.getsockname()[0]}
mac = get_mac()
doc['uuid']=mac

with open('/home/robotino/rosedge/rest_py/rob_config.json','w') as outfile:
	json.dump(doc,outfile)



put_ip = 'http PUT 10.2.1.10:8000/things < rob_config.json'

subprocess.call(put_ip, shell=True)



