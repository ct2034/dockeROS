# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:32:49 2017

@author: Poulastya_Mukherjee
"""
import remote_access_base
from remote_access_base import RemoteDock

host = 'cch-VM65N'
port = 2375

rd = RemoteDock("teleop_twist_keyboard_dockerfile", host, str(port), 'roslaunch', 'teleop_twist_keyboard',
                'teleop.launch')


def test_md5():
    assert not remote_access_base.md5checksum("teleoptwist", "teleoptwistr")


def test_create_image():
    assert rd.build_image()


def test_create_container():
    assert rd.create_docker_container()
