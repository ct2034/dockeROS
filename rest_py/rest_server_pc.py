# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:30:15 2017

@author: cch-student
"""

# sample.py
import falcon
import json
import socket
import ast
import pymongo as pymo
import datetime
from uuid import getnode as get_mac


class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        doc = {'ip_add':s.getsockname()[0]}
#        doc = {
#            'images': [
#                {
#                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
#                }
#            ],
#            'ip_add': [
#                {
#                    'add': s.getsockname()[0]
#                }
#            ]
#        }
        s.close()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(doc, ensure_ascii=False)
        
    def on_put(self, req, resp):
        print "on put"
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body','A valid JSON document is required.')
        
        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))
            request_body = req.stream.read()
            req.json = json.loads(body)
            print request_body
            
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        tmpv = ast.literal_eval(body)
        print tmpv['id']#
        client = pymo.MongoClient('localhost', 27017)
        db = client.test_database
        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}

        mac = get_mac()
        tmpv['mac_add']=mac        
        posts = db.posts
        post_id = posts.insert(tmpv)
        post_id
        print db.collection_names()
        for post in posts.find():
            print post
        #post_id
        resp.status = falcon.HTTP_201
        
        resp.body = body
        #resp.location = '/%s/things/%s' % (user_id, proper_thing['id'])

            
        #doc1 = {'ip_add1':}
#        resp.body = ('\nTwo things awe me most, the starry sky '
#                     'above me and the moral law within me.\n'
#                     '\n'
#                     '    ~ Immanuel Kant\n\n')

# falcon.API instances are callable WSGI apps
app = falcon.API()
print "sts"
# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
