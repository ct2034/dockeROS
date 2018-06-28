import os
import re
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
import sys
from debug_print import debug_eval_print
from shutil import copyfile

logging.getLogger().setLevel(logging.DEBUG)
if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
    from debug_print import debug_eval_print
else:
    def debug_eval_print(_):
        pass


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
                _update_checksum(chksum, path.dirname(
                    path), path.basename(path))

    return chksum.hexdigest()


class DockeROSImage():
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
            >>> import dockerrosimage
            >>> obj = dockerrosimage.DockeROSImage(image, ip, port, roscommand, ca_cert)
        ..  >>> obj.build_docker_image()
        ..  >>> obj.build_docker_image()
    """

    allowed_roscommands = ['roslaunch']

    def __init__(self, ip, port, roscommand, config, ca_cert=None):
        # how to reach the client?
        self.ip = ip
        self.port = port
        self.ip_str = "tcp://" + self.ip + ":" + self.port
        self.ca_cert = ca_cert

        # Version info
        logging.info("Python Version: " + sys.version)
        logging.info("docker-py Version: " + docker.__version__)

        # What is the ros command?
        self.roscommand = roscommand
        if roscommand[0] in DockeROSImage.allowed_roscommands:
            self.roscommand = roscommand[0]
        else:
            raise NotImplementedError(
                'The ros command >' + roscommand[0] + '< is currently not supported.'
            )
        self.rospackage = roscommand[1]
        self.roscommand_args = roscommand[2:]

        # Where is the package?
        rp = rospkg.RosPack()
        logging.info("\nThe config is:")
        logging.info(json.dumps(config, indent=2))
        logging.info("\n")
        self.path = rp.get_path(self.rospackage)
        self.dockeros_path = rp.get_path('dockeros')
        if self.path.startswith('/opt/ros'):
            logging.info('This is a system package at:\n> ' + self.path)
            self.user_package = False
        else:
            logging.info('This is a user package at:\n> ' + self.path)
            self.user_package = True

        # What Dockerfile should be used?
        self.dockerfile = None
        for f in os.walk(self.path):
            fname = f[0]
            if re.match(r"\/.*Dockerfile.*", fname):
                self.dockerfile = fname
                logging.info('This package has a Dockerfile at:\n> ' + self.dockerfile)
                break
        if not self.dockerfile:
            if self.user_package:
                self.dockerfile = self.dockeros_path + '/source_Dockerfile'
            else:  # system package
                self.dockerfile = self.dockeros_path + '/default_Dockerfile'
            logging.info('Using default Dockerfile:\n> ' + self.dockerfile)

        # What is the image name going to be?
        registry_string = config['registry']['host'] + \
                          ':' + str(config['registry']['port']) + '/'
        self.name = registry_string + \
                    '_'.join(self.roscommand).replace('.', '-')
        self.tag = str(path_checksum(self.path))
        logging.info("The name of the image will be: \n> " + self.name)

    def connect(self):
        """
        Connect to configured docker host
        """
        self.tls = docker.tls.TLSConfig(ca_cert=self.ca_cert) if self.ca_cert else False
        self.docker_client = docker.DockerClient(self.ip_str, tls=self.tls)

    def does_exist_on_client(self):
        """
        Checks whether a similar image exists or not
        """
        self.connect()
        images = self.docker_client.images.list()
        logging.info("Currently available images:")
        logging.info("image_names")
        for image in images:
            logging.info(image)
        image_names = map(lambda i: i.tags[0], images)
        return self.name in image_names

    def build_docker_image(self):
        """
        Compiles a baseDocker image with specific image of a rospackage
        """
        logging.info(self.path)
        copyfile(self.dockerfile, self.path + '/Dockerfile')

        # client = docker.from_env()
        # res = client.images.build(path=self.path,
        #                           tag=self.name,
        #                           buildargs={
        #                               "PACKAGE": self.rospackage
        #                           }
        #                           )
        # logging.info(res)

        cli = docker.APIClient(base_url='unix://var/run/docker.sock')
        it = cli.build(path=self.path,
                       tag=self.name + ":" + self.tag,
                       buildargs={
                           "PACKAGE": self.rospackage
                       },
                       labels={
                           "label_a": "1",
                           "label_b": "2"
                       }
                       )
        for l in it:
            ld = eval(l)
            if ld.__class__ == dict and "stream" in ld.keys():
                logging.info(ld["stream"].strip())

        # Tag as latest (rebuild ?!?)
        it = cli.build(path=self.path,
                       tag=self.name + ":" + "latest",
                       buildargs={
                           "PACKAGE": self.rospackage
                       },
                       labels={
                           "label_a": "1",
                           "label_b": "2"
                       }
                       )
        for l in it:
            ld = eval(l)
            if ld.__class__ == dict and "stream" in ld.keys():
                logging.info(ld["stream"].strip())

    def run_image(self):
        logging.info("ROS command to be executed:\n > " + " ".join(self.roscommand))
        logging.info("On Server:\n > " + ':'.join([self.ip, self.port]))

    def push_image(self):
        logging.info("to be implemented")