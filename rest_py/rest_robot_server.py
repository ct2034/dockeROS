# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:30:15 2017

@author: cch-student
"""

import falcon
import json
import socket
import ast
import datetime
from falcon_multipart.middleware import MultipartMiddleware
import psutil
import sys

"""
Server running on robot used for getting metric information about robot
for displaying in GUI. The data is not stored in database
"""
class Robmetrics(object):
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            self.ip = s.getsockname()[0]
        except Exception as e:
            print("error reaching internet")
            self.ip = '0.0.0.0'
        finally:
            s.close()
    
    """Handles GET requests"""
    def on_get(self, req, resp):
        

        doc = {'ip_add': self.ip}
        doc['cpu_usg'] = psutil.cpu_percent()
        doc['ram_usg'] = psutil.virtual_memory().percent

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(doc, ensure_ascii=False)
        
"""initializing falcon app"""
rob = falcon.API(middleware=[MultipartMiddleware()])
print("Server started successfully!")
# Resources are represented by long-lived class instances
rob_metrics = Robmetrics()

# things will handle all requests to the '/things' URL path
rob.add_route('/rob_metrics', rob_metrics)
