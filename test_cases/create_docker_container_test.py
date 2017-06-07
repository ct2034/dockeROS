# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:32:49 2017

@author: cch-student
"""

from remote_access_base import RemoteDock

host = 'cch-VM65N'
port = 2375
    
def test_answer():
    assert RemoteDock.create_docker_container("teleop_twist_keyboard_dockerfile", host, str(port), 'teleop_twist_keyboard') == True
