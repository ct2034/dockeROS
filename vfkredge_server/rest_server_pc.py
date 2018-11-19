# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:30:15 2017

@author: cch-student
"""

import falcon
from falcon_cors import CORS
import json
import ast

"""
Server class currently handles GET and PUT requests using Falcon REST API
"""


class Robconnect(object):

    def __init__(self):
        self.clients = {}
        self.clients.update(
            self.read_manual_clients()
        )
        print(self.clients)

    """Handles GET requests"""

    def on_get(self, req, resp):
        # print("on get")
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(self.clients)

    """Handles PUT requests and stores incoming data"""

    def on_put(self, req, resp):
        print("on put")
        body = req.stream.read()
        tmpv = ast.literal_eval(body)
        # tmpv['time'] = datetime.datetime.utcnow()
        print("tmpv")
        print(tmpv)
        self.clients.update({tmpv['ip']: tmpv})
        print("clients")
        print(self.clients)
        print("_________")

        # """Connecting to Database"""
        # client = pymo.MongoClient('localhost', 27017)
        # db = client.test_database

        # posts = db.posts
        # post_id = posts.insert(tmpv)
        # post_id
        # print(db.collection_names())
        # for post in posts.find():
        #     print(post)

        resp.status = falcon.HTTP_201
        resp.body = "OK!"

    def read_manual_clients(self):
        file_path = 'manual_clients.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data


"""initializing falcon app"""
cors = CORS(allow_all_origins=True)
app = falcon.API(middleware=[cors.middleware])
print("Server started successfully!")
# Resources are represented by long-lived class instances
things = Robconnect()

# things will handle all requests to the '/things' URL path
app.add_route('/clients', things)
