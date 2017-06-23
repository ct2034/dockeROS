# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:32:30 2017

@author: cch-student
"""

import pymongo as pymo
import datetime
import subprocess
import os
import ast
from uuid import getnode as get_mac

get_ip = 'http 10.2.1.11:8000/things >> tmpfile'
subprocess.call(get_ip, shell=True)
pathtmpfile = os.path.abspath("tmpfile")


tmpfile = open(pathtmpfile, "r")
pkg_path = tmpfile.read()
tmpfile.close()
os.remove(pathtmpfile)
dict_pkp = ast.literal_eval(pkg_path)
print dict_pkp['ip_add']
mac = get_mac()
dict_pkp['mac_add']=mac
#dict_pkp_lvl2 = (dict_pkp['ip_add'])#ast.literal_eval(dict_pkp['ip_add'])
#print dict_pkp['ip_add']
#dict_pkp_lvl2 = ast.literal_eval(tmp)
#print dict_pkp_lvl2['add']
#print pkg_path['ip_add']# = pkg_path[:-1]




client = pymo.MongoClient('localhost', 27017)
db = client.test_database
post = {"author": "Mike",
       "text": "My first blog post!",
       "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert(dict_pkp)
post_id

print db.collection_names()

print "################################"
for post in posts.find():
    print post
