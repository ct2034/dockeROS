import subprocess
import docker
import os
import shutil

from remote_access_base import RemoteDock

host = 'cch-VM65N'
port = 2375

def test_answer():
    assert RemoteDock.create_docker_image("teleop_twist_keyboard_dockerfile", host, str(port), 'teleop_twist_keyboard') == False
