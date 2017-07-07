# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:44:45 2017

@author: Poulastya_Mukherjee
"""

import os
import socket
import subprocess
import threading
import hashlib
import docker
import shutil
from os import path
import json

import logging
import rospkg
from debug_print import debug_eval_print


class MltThrd(threading.Thread):
    def __init__(self, cmd, queue):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.queue = queue

    def run(self):
        # execute the command, queue the result
        subprocess.call(self.cmd, shell=True)

def compare(str1, str2):
    """
        Compares two input strings and returns true or false after running
        md5 checksum algorithm
        Args:
            str1 (str): 1st string
            str1 (str): 2nd string      
    """
    m1 = hashlib.md5()
    m2 = hashlib.md5()
    m1.update(str1)
    m2.update(str2)
    return m1.digest() == m2.digest()

def path_checksum(this_path):
    """
    Recursively calculates a checksum representing the contents of all files
    found with a sequence of file and/or directory paths.
    Source: https://code.activestate.com/recipes/576973-getting-the-sha-1-or-md5-hash-of-a-directory/#c3

    """
    paths = [this_path]
    if not hasattr(paths, '__iter__'):
        raise TypeError('sequence or iterable expected not %r!' % type(paths))

    def _update_checksum(checksum, dirname, filenames):
        for filename in sorted(filenames):
            this_path = path.join(dirname, filename)
            if path.isfile(this_path):
                logging.debug(path)
                fh = open(this_path, 'rb')
                while 1:
                    buf = fh.read(4096)
                    if not buf:
                        break
                    checksum.update(buf)
                fh.close()

    chksum = hashlib.sha1()

    for p in sorted([path.normpath(f) for f in paths]):
        if path.exists(p):
            if path.isdir(p):
                path.walk(p, _update_checksum, chksum)
            elif path.isfile(path):
                _update_checksum(chksum, path.dirname(path), path.basename(path))

    return chksum.hexdigest()

class RemoteDock():
    """
        Remotely deploys a docker container with a user specified image of a 
        rospackage
        Args:
            image (str): the image is created with user input + '_dockerfile'
            ip (str): IP address of the robot on which the container should run
            port (str): Port on which docker demon is running, check from robot
            roscommand (str): e.g. roslaunch or rosrun based on type of ros 
            package file
            rospackage (str): the user specified rospackage which should run
            roslaunchfile (str) : the specific ros file to be run
            
        Example:
            >>> import remote_access_base
            >>> obj = remlib.RemoteDock(image, ip, port, roscommand, rospackage, roslaunchfile, ca_cert)
        ..  >>> obj.startcheck()
    """

    allowed_roscommands = ['roslaunch']

    def __init__(self, ip, port, roscommand, config, ca_cert=None,
                 path_=('This is a system package at:\n> ' + self.path)):
        # how to reach the client?
        self.ip = ip
        self.port = port
        self.ip_str = "tcp://" + self.ip + ":" + self.port
        self.tls = docker.tls.TLSConfig(ca_cert=ca_cert) if ca_cert else False
        self.docker_client = docker.DockerClient(self.ip_str, tls=self.tls)
        # What is the ros command?
        command = roscommand.split(' ')
        if command[0] in RemoteDock.allowed_roscommands:
            self.roscommand = command[0]
        else:
            raise NotImplementedError('The ros command >'+command[0]+'< is currently not supported.')
        self.rospackage = command[1]
        self.roslaunchfile = command[2]
        # What is the image name going to be?
        rp = rospkg.RosPack()
        print("\nThe config is:")
        print(json.dumps(config, indent=2))
        print("\n")
        self.path = rp.get_path(self.rospackage)
        self.rosedge_path = rp.get_path('rosedge')
        if self.path.startswith('/opt/ros'):
            print path_
            self.user_package = False
        else:
            print('This is a user package at:\n> ' + self.path)
            self.user_package = True
        self.dockerfile = None
        for f in os.walk(self.path):
            fname = f[0]
            if fname.endswith('/Dockerfile'):
                self.dockerfile = fname
                print('This package has a Dockerfile at:\n> ' + self.dockerfile)
                break
        if not self.dockerfile:
            if self.user_package:
                self.dockerfile = self.rosedge_path + '/source_Dockerfile'
            else:  # system package
                self.dockerfile = self.rosedge_path + '/default_Dockerfile'
            print('Using default Dockerfile:\n> ' + self.dockerfile)

        registry_string = config['registry']['host'] + ':' + str(config['registry']['port']) + '/'
        self.name = registry_string + \
                    '_'.join(command).replace('.', '_') + \
                    ':' + str(path_checksum(self.path))

        print("The name of the image will be: \n> " + self.name)


    def does_exist_on_client(self):
        """
        Checks whether a similar image exists or not
        """
        images = self.docker_client.images.list()
        print("Currently available images:")
        print("image_names")
        image_names = map(lambda i: i.tags[0], images)
        return self.name in image_names
    
    
    def create_docker_image(self):
        """
        Compiles a baseDocker image with specific image of a rospackage and 
        deploys the built image on the server
        """
        # reading base docker commands


        copysh_path = os.path.abspath("basedocker") + "/ros_entrypoint.sh"
        base_path = os.path.abspath("basedocker") + "/Dockerfile"
        rd_base = open(base_path, "r")
        contents = rd_base.readlines()
        rd_base.close()

        # reading docker file of specific launch files from ros packages
        folder_cmd = "find ~ -type d -name " + self.rospackage + "_Dockerfile >> tmpfile" 
        subprocess.call(folder_cmd, shell=True)
        pathtmpfile = os.path.abspath("tmpfile")
        tmpfile = open(pathtmpfile, "r")
        pkg_path = tmpfile.read()
        tmpfile.close()
        pkg_path = pkg_path[:-1]
        os.remove(pathtmpfile)
        pkg_path = pkg_path + "/Dockerfile"
        dock_read = open(pkg_path, "r")
        tmp_contents = dock_read.readlines()
        dock_read.close()
        idx = 9
        
        for i in range(len(tmp_contents)):
            contents.insert(idx, tmp_contents[i])
            idx = idx + 1
    
        os.mkdir(self.rospackage + "_docker")
        tmppath = os.getcwd() + '/' + self.rospackage + "_docker"
        tmentrysh = tmppath +  "/ros_entrypoint.sh"
        shutil.copyfile(copysh_path,tmentrysh)
        os.chdir(tmppath)
        make_exec = "chmod +x ros_entrypoint.sh"
        subprocess.call(make_exec,shell=True)
        file = open('Dockerfile', 'w')
        contents = "".join(contents)
        file.write(contents)
        file.close()
        tarcode = "tar zcf Dockerfile.tar.gz Dockerfile ros_entrypoint.sh"
        subprocess.call(tarcode, shell=True)
        buildcode = "curl -v -X POST -H " + '"Content-Type:application/tar"' + \
            " --data-binary '@Dockerfile.tar.gz' http://" + self.ip + ":" + \
            self.port + "/build?t=" + self.image        
        status = subprocess.call(buildcode, shell=True)
        return status
    
    
    def create_docker_container(self):
        """
        Creates a Docker container and uses the image built from function 
        createDockerImg and deploys it directly on the server
        """
        cli = docker.Client(base_url=self.ip_str)
        container = cli.create_container(self.image,
                                         hostname='3e93a4b05cf6',
                                         user='1000:1000',
                                         stdin_open=True,
                                         tty=True,
                                         entrypoint='/ros_entrypoint.sh',
                                         command=["bash"],
                                         environment=[
                                             "PATH/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
                                         working_dir='/',
                                         volumes='$HOME/.config/catkin:/.config/catkin:ro')
        cli.start(container['Id'])
        self.container_id = container['Id']
        return container['Id']
    
        
    def run_docker_commands(self):
        """
        Runs the created docker container using the generated container id 
        from createDockerContainer function
        """
        cli = docker.Client(base_url=self.ip_str)
        rosip_str = cli.inspect_container(self.container_id)['NetworkSettings']['IPAddress']
        dockerexec_source = "docker -H tcp://" + self.ip + ":" + \
        self.port + " exec -it " + self.container_id + " bash -c \
        'source ros_entrypoint.sh;export ROS_MASTER_URI=http://'" + self.ip + "':11311;\
        export ROS_IP='"+ rosip_str +"';'" + self.roscommand + "' '" + self.rospackage + "' '" \
        + self.roslaunchfile
        subprocess.call(dockerexec_source,shell=True)
    
      
    def run_existing_image(self):
        """
        Runs the existing image in the local machine on the robot
        """
        dockercmd_runimg = "docker -H tcp://" + self.ip + ":" + self.port + " run -it --rm -u " + \
                            '"$(id -u):$(id -g)" ' + \
                            "-v $HOME/.ros:/.ros -v $HOME/.config/catkin:/.config/catkin:ro " + \
                            "-v $(pwd):$(pwd) -w $(pwd) " + self.image
        
        subprocess.call(dockercmd_runimg, shell=True)
