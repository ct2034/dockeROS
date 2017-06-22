# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:30:15 2017

@author: cch-student
"""

# sample.py
import falcon
import json
import socket

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
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
#        resp.body = ('\nTwo things awe me most, the starry sky '
#                     'above me and the moral law within me.\n'
#                     '\n'
#                     '    ~ Immanuel Kant\n\n')

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
