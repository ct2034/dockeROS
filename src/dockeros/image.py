import os
import re
import subprocess
import docker
import json
import logging
import rospkg
import sys

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

        Example:
            >>> import image
            >>> obj = image.DockeROSImage(roscommand, config)
            >>> obj.make_client()
            >>> obj.build()
            >>> obj.run()
    """

    def __init__(self, roscommand, config, dockerfile=None):
        """
            Initilizes the commands with the rospkg configuration and roscommands allowed in this context
            Args:
                roscommand: any of suppoorted roscommands (rosrun/roslaunch)
                config: configuraion for rospkg and connection to docker host
        """
        # how to reach the client?
        # Version info
        logging.debug("Python Version: " + sys.version + "\ndocker (library) Version: " + docker.__version__)

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
        logging.debug("The config is:\n"+json.dumps(config, indent=2))
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

        if self.path: # on system
            if self.path.startswith('/opt/ros'):
                self.check_rosdep()
                logging.info('This is a system package to be installed from:\n> ' + self.deb_package)
                self.user_package = False
            else:
                logging.info('This is a user package at:\n> ' + self.path)
                self.user_package = True

        # What Dockerfile should be used?
        self.dockerfile = None
        if dockerfile: # defined by cli
            self.dockerfile = dockerfile
        elif self.path: # in package folder
            for fs in os.walk(self.path):
                for f in fs[2]:
                    fname = fs[0] + "/" + f
                    if re.match(r".*Dockerfile.*", f):
                        self.dockerfile = fname
                        logging.info('This package has a Dockerfile at:\n> ' + self.dockerfile)
                        break
        if not self.dockerfile:
            logging.info('This package does not have a Dockerfile')
            if self.user_package:
                self.dockerfile = self.dockeros_path + '/config/source_Dockerfile'
                logging.info('Using source Dockerfile:\n> ' + self.dockerfile)
            else:  # system package
                self.dockerfile = self.dockeros_path + '/config/default_Dockerfile'
                logging.info('Using default Dockerfile:\n> ' + self.dockerfile)

        # What is the image name going to be?
        if "registry" in config.keys():
            self.registry_string = config['registry'] + '/'
        else:
            self.registry_string = ""
        self.name = "_".join(self.roscommand).replace('.', '-')
        self.tag = self.registry_string + self.name
        logging.info("name: \n> " + self.name)
        logging.info("tag: \n> " + self.tag)

        # The actual image:
        self.image = None

    def check_rosdep(self):
        """
        Checking system dependencies required by ROS packages
        """
        out = subprocess.check_output(
            " ".join(
                ["rosdep", "resolve", self.rospackage]),
            shell=True)
        logging.debug(out)
        self.deb_package = out.split("\n")[1].strip()

    def build(self):
        """
        Compiles a baseDocker image with specific image of a rospackage
        """
        TMP_DF_PATH = '/tmp/tmp_Dockerfile'
        if self.user_package:
            user_dockerfile_path = self.path + "/Dockerfile"
            with open(self.dockerfile, 'r') as in_file:
                with open(user_dockerfile_path, 'w+') as out_file:
                    out_file.truncate()
                    for l in in_file:
                        l = l.replace("#####ROS_PACKAGE#####", self.rospackage)
                        l = l.replace("#####CMD#####", "[\""+"\", \"".join(
                            ["/ros_entrypoint.sh"] + self.roscommand
                        )+"\"]" )
                        out_file.write(l)
                    out_file.close()

            if DEBUG:
                with open(user_dockerfile_path, 'r') as dockerfile:
                    print "Dockerfile used: ############################################"
                    for l in dockerfile:
                        print l.strip()
                    print "#############################################################"

            with open(user_dockerfile_path, 'r') as dockerfile:
                self.image, it = self.docker_client.images.build(
                    path=self.path,
                    tag=self.tag
                    )
                for l in it:
                    print('| '+(l['stream'].strip() if ('stream' in l.keys()) else ''))
                logging.info("Image was created. Tags are: " + ', '.join(self.image.tags))

        else:
            assert self.deb_package, "Debian package needs to be available"
            with open(self.dockerfile, 'r') as in_file:
                with open(TMP_DF_PATH, 'w+') as out_file:
                    out_file.truncate()
                    for l in in_file:
                        l = l.replace("#####DEB_PACKAGE#####", self.deb_package)
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
                self.image, it = self.docker_client.images.build(
                    fileobj=dockerfile,
                    custom_context=False,
                    tag=self.tag
                    )
                for l in it:
                    print('| '+(l['stream'].strip() if ('stream' in l.keys()) else ''))
                logging.info("Image was created. Tags are: " + ', '.join(self.image.tags))

    def run(self):
        """
        Run the Image on Host
        """
        logging.info("Starting:\n > " + " ".join(self.roscommand) + " <")
        self.docker_client.containers.run(
            image=self.tag,
            name=self.name,
            network='host',
            detach=True
            )

    def stop(self):
        """
        Stop the container
        """
        logging.info("Stopping:\n > " + " ".join(self.roscommand) + " <")
        try:
            cont = self.docker_client.containers.get(self.name)
            try:
                cont.stop()
            except Exception as e:
                cont.kill()
                logging.error(e)
            cont.remove()
            logging.info("Removed:\n > " + " ".join(self.roscommand) + " <")
        except Exception as e:
            logging.error(e)

    def push(self):
        """
        Push the image to a registry defined in the config
        """
        if not self.registry_string:
            logging.error("Your config has no registry. Pushing makes no sense.")
        else:
            stream = self.docker_client.images.push(self.tag, stream=True)
            for l in stream:
                print(l)


    def make_client(self, ip=None, port=None):
        """
        Initialize a docker client either using local or remote docker deamon.
        When you give no parameters, the local enviornment is used.
        So either your local deamon or the one defined in the DOCKER_HOST environment variable.(see https://dockr.ly/2zMPc17 for details)
        (see https://dockr.ly/2zMPc17 for details)
        Args:
            ip: ip or host of the remote deamon (give None to use local environment)
            port: port of the remote deamon
        """
        if not ip:
            self.docker_client=docker.from_env()
        else:
            self.docker_client=docker.client("tcp:/"+":".join([ip.strip(), port.strip()]))
