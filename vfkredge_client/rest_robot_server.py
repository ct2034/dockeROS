# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:30:15 2017

@author: cch-student
"""

import falcon
import json
import socket
from falcon_cors import CORS
import psutil
import requests

"""
Server running on robot used for getting metric information about robot
for displaying in GUI. The data is not stored in database
"""


class Robmetrics(object):
    def __init__(self):
        self.config = self.read_config()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((self.config["server_host"], 8080))
            self.ip = s.getsockname()[0]
        except Exception as e:
            print("error reaching " + self.config["server_host"])
            self.ip = '0.0.0.0'
        finally:
            s.close()
        self.register_data = {
            "name": self.config['my_name'],
            "ip": self.ip
        }
        r = requests.put(
            'http://'+
            self.config["server_host"]+
            ':5004/things', 
            data=json.dumps(self.register_data))
        print(r.status_code)

    """Reading config"""

    def read_config(self):
        file_path = 'rob_config.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    """Handles GET requests"""

    def on_get(self, req, resp):
        doc = self.register_data
        doc['cpu_usg'] = psutil.cpu_percent()
        doc['ram_usg'] = psutil.virtual_memory().percent

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(doc, ensure_ascii=False)


"""initializing falcon app"""
cors = CORS(allow_all_origins=True)
api = falcon.API(middleware=[cors.middleware])
print("Server started successfully!")
# Resources are represented by long-lived class instances
rob_metrics = Robmetrics()
api.add_route('/rob_metrics', rob_metrics)
