# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:59:25 2017

@author: cch-student
"""

import falcon

from .images import Resource


api = application = falcon.API()

images = Resource()
api.add_route('/images', images)