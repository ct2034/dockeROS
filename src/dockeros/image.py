import os
import re
import subprocess
import docker
import json
import logging
import rospkg
import sys

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("docker").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
    def debug_eval_print(a):
        print(a)
    DEBUG = True
else:
    def debug_eval_print(_):
        pass
    DEBUG = False


def _get_allowed_roscommands():
    return ['roslaunch', 'rosrun']


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
            >>> import image
            >>> obj = image.DockeROSImage(image, ip, port, roscommand, ca_cert)
        ..  >>> obj.build_docker_image()
        ..  >>> obj.build_docker_image()
    """

    def __init__(self, roscommand, config):
        """
            Initilizes the commands with the rospkg configuration and roscommands allowed in this context
            Args:
                roscommand: any of suppoorted roscommands (rosrun/roslaunch) [Also:_get_allowed_roscommands]
                config: configuraion for rospkg

        """
        # how to reach the client?

        # Version info
        logging.info("Python Version: " + sys.version + "\ndocker (library) Version: " + docker.__version__)

        # What is the ros command?
        assert isinstance(roscommand, list), "roscommand should be a list"
        assert isinstance(roscommand[0], str), "roscommand should be a list of strings"
        self.roscommand = roscommand
        if roscommand[0] in _get_allowed_roscommands():
            self.roscommand = roscommand[:]
            self.rospackage = roscommand[1]
        else:
            raise NotImplementedError(
                'The ros command >' + roscommand[0] + '< is currently not supported.'
            )

        # Where is the package?
        rp = rospkg.RosPack()
        logging.info("The config is:\n"+json.dumps(config, indent=2))
        self.dockeros_path = rp.get_path('dockeros')

        self.path = None
        try:
            self.path = rp.get_path(self.rospackage)
        except rospkg.common.ResourceNotFound as e:
            try:
                self.check_rosdep()
                logging.info('This is a system package to be installed from:\n> ' + self.deb_package)
                self.user_package = False
            except:
                raise e

        if self.path: # on systemS
            if self.path.startswith('/opt/ros'):
                self.check_rosdep()
                logging.info('This is a system package to be installed from:\n> ' + self.deb_package)
                self.user_package = False
            else:
                logging.info('This is a user package at:\n> ' + self.path)
                self.user_package = True

        # What Dockerfile should be used?
        self.dockerfile = None
        if self.path:
            for f in os.walk(self.path):
                fname = f[0]
                if re.match(r"\/.*Dockerfile.*", fname):
                    self.dockerfile = fname
                    logging.info('This package has a Dockerfile at:\n> ' + self.dockerfile)
                    break
        if not self.dockerfile:
            if self.user_package:
                self.dockerfile = self.dockeros_path + '/config/source_Dockerfile'
            else:  # system package
                self.dockerfile = self.dockeros_path + '/config/default_Dockerfile'
            logging.info('Using default Dockerfile:\n> ' + self.dockerfile)

        # What is the image name going to be?
        self.registry_string = config['registry']['host'] + \
                          ':' + str(config['registry']['port']) + '/'
        self.name = "_".join(self.roscommand).replace('.', '-')
        self.tag = "latest"
        logging.info("The name of the image will be: \n> " + self.name)

        # The actual image:
        self.image = None

    def check_rosdep(self):
        """
            Checking system dependencies required by ROS packages
        """
        out = subprocess.check_output(
            " ".join(
                ["rosdep", "resolve", self.rospackage, "--os=ubuntu:xenial"]),
            # TODO: dynamic os definition
            shell=True)
        logging.debug(out)
        self.deb_package = out.split("\n")[1].strip()

    def connect(self, ip, port, ca_cert=None):
        """
        Connect to configured docker host
        """
        self.ip = ip
        self.port = port
        self.ip_str = "tcp://" + self.ip + ":" + self.port
        self.ca_cert = ca_cert
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

    def build_image(self):
        """
        Compiles a baseDocker image with specific image of a rospackage
        """
        TMP_DF_PATH = '/tmp/tmp_Dockerfile'
        client = docker.from_env()
        if self.user_package:
            try:
                in_file = open(self.dockerfile, 'r')
                it = client.images.build(path=self.path,
                               tag=self.name + ":" + self.tag,
                               dockerfile=self.dockerfile,
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
            except Exception  as e:
                logging.error("Exception during building:" + str(e))
            finally:
                in_file.close()
        else:
            assert self.deb_package, "Debian package needs to be available"
            if True:
                with open(self.dockerfile, 'r') as in_file:
                    with open(TMP_DF_PATH, 'w+') as out_file:
                        out_file.truncate()
                        for l in in_file:
                            l = l.replace("#####DEB_PACKAGE#####", self.deb_package)
                            l = l.replace("#####ROS_MASTER_URI#####", "http://172.17.0.1:11311") # TODO: config
                            l = l.replace("#####CMD#####", "[\""+"\", \"".join(
                                ["/ros_entrypoint.sh"] + self.roscommand
                            )+"\"]" )
                            out_file.write(l)
                        out_file.close()

                if DEBUG:
                    with open(TMP_DF_PATH, 'r') as dockerfile:
                        print "Dockerfile used: ############################################"
                        for l in dockerfile:
                            print l.strip()
                        print "#############################################################"

                with open(TMP_DF_PATH, 'r') as dockerfile:
                    self.image, it = client.images.build(
                        fileobj=dockerfile,
                        custom_context=False,
                        tag=self.name + ":" + self.tag
                        )
                    for l in it:
                        print('| '+(l['stream'].strip() if ('stream' in l.keys()) else ''))
                    logging.info("Image was created. Tags are: " + ', '.join(self.image.tags))

    def run_image(self, ip=None, port=None):
        logging.info("ROS command to be executed:\n > " + " ".join(self.roscommand))
        client = self.make_client(ip, port)
        client.containers.run(
            image=self.name,
            name=self.name,
            network='host'
            )

    def make_client(self, ip=None, port=None):
        return docker.from_env()

    def push_image(self):
        client = docker.from_env()
