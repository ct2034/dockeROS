# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:44:45 2017

@author: cch-student
"""

import os
import subprocess
import sys
import threading
import Queue
import commands
import time
import socket
import md5
import docker
import shutil


class MltThrd(threading.Thread):
    def __init__(self, cmd, queue):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.queue = queue

    def run(self):
        # execute the command, queue the result
        subprocess.call(self.cmd, shell=True)
        # (status, output) = commands.getstatusoutput(self.cmd)
        # self.queue.put((self.cmd, output, status))


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def md5checksum(str1, str2):
    m1 = md5.new()
    m2 = md5.new()
    m1.update(str1)
    m2.update(str2)
    if (m1.digest() == m2.digest()):
        return True
    else:
        return False


def createDockerImg(image, ip, rospackage):

    ip_str = "tcp://" + ip + ":2375"
    cli = docker.Client(base_url=ip_str)    
    # reading base docker commands
    print "Docker file does not exist. Creating docker file..."
    copysh_path = os.path.abspath("basedocker") + "/ros_entrypoint.sh"
    
    base_path = os.path.abspath("basedocker") + "/Dockerfile"
    rd_base = open(base_path, "r")
    contents = rd_base.readlines()
    rd_base.close()

    # reading docker file of specific launch files from ros packages
    folder_cmd = "find ~ -type d -name " + rospackage + "_Dockerfile >> tmpfile" #"rospack find " + rospackage + " >> tmpfile"
    subprocess.call(folder_cmd, shell=True)
    pathtmpfile = os.path.abspath("tmpfile")
    tmpfile = open(pathtmpfile, "r")
    pkg_path = tmpfile.read()
    tmpfile.close()
    pkg_path = pkg_path[:-1]
    os.remove(pathtmpfile)
    pkg_path = pkg_path + "/Dockerfile"
    print "!!!!!!!!!!"
    print pkg_path
    dock_read = open(pkg_path, "r")
    tmp_contents = dock_read.readlines()
    dock_read.close()
    idx = 9
    for i in range(len(tmp_contents)):
        contents.insert(idx, tmp_contents[i])
        idx = idx + 1

    # pkgdocker = op
    os.mkdir(rospackage + "_docker")
    tmppath = os.getcwd() + '/' + rospackage + "_docker"
    print tmppath
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
        " --data-binary '@Dockerfile.tar.gz' http://" + ip + ":2375/build?t=" + image
            
    subprocess.call(buildcode, shell=True)
    #cli.build(fileobj=tmppath+'')

def createDockerContainer(image, ip, roscommand, rospackage, roslaunchfile, dockercmd_rosmaster, dockercmd_rosip):

    ip_str = "tcp://" + ip + ":2375"
    cli = docker.Client(base_url=ip_str)
    container = cli.create_container(image,
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
    # cmd_id_rm = cli.exec_create(container['Id'],dockercmd_rosmaster)
    # cli.exec_start(cmd_id_rm)
    # cmd_id_ip = cli.exec_create(container['Id'],dockercmd_rosip)
    # cli.exec_start(cmd_id_ip)
    # ros_cmd = roscommand + ' ' + rospackage + ' ' + roslaunchfile
    bash_cmd = "docker -H tcp://" + ip + \
        ":2375 exec -it " + container['Id'] + " /bin/bash"
    bash_cmd = '/bin/bash'
    print bash_cmd
    return container['Id']
    #cmd_id = cli.exec_create(container['Id'], bash_cmd)

    #cli.exec_start(cmd_id)

def runDockerCommands(container_id,ip,roscommand,rospackage,roslaunchfile):
    
    print ip
    print container_id
    ip_str = "tcp://" + ip + ":2375"
    cli = docker.Client(base_url=ip_str)
    rosip_str = cli.inspect_container(container_id)['NetworkSettings']['IPAddress']
    
    dockerexec_source = "docker -H tcp://" + ip + ":2375 exec -it " + container_id + " bash -c \
    'source ros_entrypoint.sh;export ROS_MASTER_URI=http://'" + ip + "':11311;\
    export ROS_IP='"+ rosip_str +"';'" + roscommand + "' '" + rospackage + "' '" \
    + roslaunchfile
    
    subprocess.call(dockerexec_source,shell=True)

try:
    ip = sys.argv[1]
except:
    print "IP address not entered!exiting script"
    exit()

try:
    roscommand = sys.argv[2]
except:
    print "Ros command not entered!exiting script"
    exit()

try:
    rospackage = sys.argv[3]
except:
    print "Ros package name not entered!exiting script"
    exit()

try:
    roslaunchfile = sys.argv[4]
except:
    print "Ros launch file name not entered!exiting script"
    exit()


dockercmd_img = "docker -H tcp://" + ip + ":2375 images"
subprocess.call(dockercmd_img, shell=True)
# image = raw_input("Enter docker image name from list:")
image = rospackage + "_dockerfile"
dockercmd_getimages = "curl -v http://" + ip + \
    ":2375/images/search?term=" + image + " | jq '.[] | .name' >> tmpfile"
subprocess.call(dockercmd_getimages, shell=True)
pathtmpfile = os.path.abspath("tmpfile")
tmpfile = open(pathtmpfile, "r")
img_nm = tmpfile.read()
img_nm = img_nm[1:-2]
print img_nm
os.remove(pathtmpfile)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
ros_ip = s.getsockname()[0]


dockercmd_runimg = "docker -H tcp://" + ip + ":2375 run -it --rm -u " + \
    '"$(id -u):$(id -g)" ' + \
    "-v $HOME/.ros:/.ros -v $HOME/.config/catkin:/.config/catkin:ro " + \
    "-v $(pwd):$(pwd) -w $(pwd) " + \
    image
docker_exec_str = "docker -H tcp://" + ip + ":2375 " + \
    "exec $(docker -H tcp://" + ip + ":2375 ps -q) "
dockercmd_getconid = docker_exec_str + "ls"
dockercmd_rosmaster = docker_exec_str + \
    "export ROS_MASTER_URI=http://" + ip + ":11311"
dockercmd_rosip = docker_exec_str + "export ROS_IP=" + ros_ip
dockercmd_teleop = docker_exec_str + ""

var = md5checksum(image, img_nm)
if not var:
    createDockerImg(image, ip, rospackage)
    cont_id = createDockerContainer(image, ip, roscommand, rospackage,
                          roslaunchfile, dockercmd_rosmaster, dockercmd_rosip)
    print cont_id                     
    runDockerCommands(cont_id,ip,roscommand,rospackage,roslaunchfile)

else:
    cmds = [dockercmd_runimg]
    try:

        result_queue = Queue.Queue()
        # subprocess.call(cmds[0], shell=True)
        for cmd in cmds:
            thread = MltThrd(cmd, result_queue)
            thread.start()
            time.sleep(2)

    except:
        print "Exiting script! Error in Execution!"
        exit()
