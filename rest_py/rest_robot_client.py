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
import time
import psutil
import sys

def connect_server(put_ip):
    subprocess.call(put_ip, shell=True)
  
"""configurable server ip"""
server_ip = '10.2.1.10'

var = 3
"""Getting IP address """
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
doc = {'ip_add':s.getsockname()[0]}

"""Getting mac address for uuid"""
mac = get_mac()
doc['uuid']=mac

"""
If 'mem' keyword is passed as argument to this script,
the memory information of the robot is sent as PUT
"""
try:
    is_mem_info = sys.argv[1]
    
except: 
    is_mem_info = "config"
    
if is_mem_info == "mem":
    doc['cpu_usg'] = psutil.cpu_percent()
    doc['ram_usg'] = psutil.virtual_memory()

"""Writing a JSON file"""
file_path = '/home/robotino/rosedge/rest_py/rob_config.json'
file_path = '/home/cch-student/rosedge/rest_py/rob_config.json'

with open(file_path,'w') as outfile:
	json.dump(doc,outfile)

"""Sending Json command to Server Robot"""
put_ip = 'http PUT ' + server_ip + ':8000/things < rob_config.json'
put_ip = 'http PUT localhost:8000/things < rob_config.json'

try:
    subprocess.call(put_ip, shell=True)

except falcon.HTTP_503:
    print "Attempting to reconnect in 10 secs.."
    print "61!"
    time.sleep(10)
    #var = connect_server(put_ip)
    while var != 0:
        time.sleep(10)
        var = connect_server(put_ip)