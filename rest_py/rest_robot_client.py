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

server = "172.0.0.1"

"""Getting IP address """
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((server, 80))
doc = {'ip_add': s.getsockname()[0]}

"""Getting mac address for uuid"""
mac = get_mac()
doc['uuid'] = mac

"""Writing a JSON file"""
with open('/tmp/rob_config.json', 'w') as outfile:
    json.dump(doc, outfile)

"""Sending Json command to Server Robot"""
put_ip = 'curl -i -X PUT %s:8000/things < /tmp/rob_config.json' % server
subprocess.call(put_ip, shell=True)
