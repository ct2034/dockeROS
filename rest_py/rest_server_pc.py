# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:30:15 2017

@author: cch-student
"""

import falcon
import json
import socket
import ast
import pymongo as pymo
import datetime
from falcon_multipart.middleware import MultipartMiddleware

class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        doc = {'ip_add':s.getsockname()[0]}
        s.close()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(doc, ensure_ascii=False)
        
    def on_put(self, req, resp):
        print "on put"
        print req.get_param('uuid')
        body = req.stream.read()
        print "on put1"
        if not body:
            raise falcon.HTTPBadRequest('Empty request body','A valid JSON document is required.')
        
        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))
            print "on put2"
            request_body = req.stream.read()
            print "on put3"
            req.json = json.loads(body)
            print "on put4"
            print request_body
            
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        tmpv = ast.literal_eval(body)
        client = pymo.MongoClient('localhost', 27017)
        db = client.test_database
        

        tmpv['time'] = datetime.datetime.utcnow()
        posts = db.posts
        post_id = posts.insert(tmpv)
        post_id
        print db.collection_names()
        for post in posts.find():
            print post
        #post_id
        resp.status = falcon.HTTP_201
        
        resp.body = "OK!"

# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[MultipartMiddleware()])
print "sts"
# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
