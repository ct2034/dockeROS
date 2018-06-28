import subprocess
import sys
import remote_access_base
import logging
import yaml
import rospkg
import rospy

logging.getLogger('root').setLevel(logging.DEBUG)
if logging.getLogger('root').getEffectiveLevel() == logging.DEBUG:
    from debug_print import debug_eval_print
else:
    def debug_eval_print(_):
        pass

usage = "USAGE:\n" + \
        "," * 80 + "\n" \
        "$ dockeROS <build/run> <IP:Port> roslaunch ros_naviagtion move_base.launch\n" \
        "Will perform the ros command in a docker container at the mentioned IP\n" + \
        "'" * 80 + "\n" \

def dummy():
    rospy.loginfo("to be implemented ..")

commands = {
    "build": dummy,
    "run": dummy,
    "push": dummy
}

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    rospy.loginfo(proc_stdout)

try:
    command = sys.argv[1]
    if not command in commands.keys():
        raise Exception()
except:
    rospy.loginfo(usage)
    rospy.error("No valid command")
    exit()

if command == "build":  # no ip needed
    try:
        roscommand = sys.argv[2:]
        ip = ""
        port = ""
    except:
        rospy.loginfo(usage)
        rospy.error("Ros command not entered! exiting script")
        exit()

else:  # ip needed
    try:
        ip_and_port = sys.argv[2]
        ip = ip_and_port.split(':')[0]
        port = ip_and_port.split(':')[1]
    except:
        rospy.loginfo(usage)
        rospy.error("Host and/or port not entered! exiting script")
        exit()

    try:
        roscommand = sys.argv[3:]
    except:
        rospy.loginfo(usage)
        rospy.logerror("Ros command not entered! exiting script")
        exit()

rp = rospkg.RosPack()
fname = rp.get_path('dockeros') + '/config.yaml'
config = yaml.load(open(fname))
dock_obj = remote_access_base.RemoteDock(ip, port,
                                         roscommand,
                                         config=config,
                                         ca_cert='/home/cch/.docker/ca.pem')

commands["build"] = dock_obj.build_docker_image
commands["run"] = dock_obj.run_docker_image

try:
    commands[command]()
except Exception as e:
    rospy.logerror("Failed to execute command")
    rospy.logerror(e)
    exit()


# if not dock_obj.does_exist_on_client():
# else:
#     dock_obj.run_existing_image()
