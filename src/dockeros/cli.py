import subprocess
import sys
import image
import logging
import yaml
import rospkg

logging.getLogger('root').setLevel(logging.DEBUG)
if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
    pass
else:
    def debug_eval_print(_):
        pass

usage = "USAGE:\n" + \
        "," * 80 + "\n" \
        "$ dr <build/run> <IP:Port> roslaunch ros_naviagtion move_base.launch\n" \
        "Will perform the ros command in a docker container at the mentioned IP\n" + \
        "'" * 80 + "\n" \

def dummy():
    logging.info("to be implemented ..")

commands = {
    "build": dummy,
    "run": dummy,
    "push": dummy,
    "_get_allowed_roscommands": dummy,
}

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    logging.info(proc_stdout)

command = ""
try:
    command = sys.argv[1]
except:
    logging.info(usage)
    exit()

if command == "_get_allowed_roscommands":
    print(" ".join(image._get_allowed_roscommands()))
    exit()
elif command == "build" or command == "push":  # no ip needed
    try:
        roscommand = sys.argv[2:]
        ip = ""
        port = ""
    except:
        logging.info(usage)
        logging.error("Ros command not entered! exiting script")
        exit()
elif command == "run":  # ip needed
    try:
        ip_and_port = sys.argv[2]
        ip = ip_and_port.split(':')[0]
        port = ip_and_port.split(':')[1]
    except:
        logging.info(usage)
        logging.error("Host and/or port not entered! exiting script")
        exit()

    try:
        roscommand = sys.argv[3:]
    except:
        logging.info(usage)
        logging.error("Ros command not entered! exiting script")
        exit()
else:
    logging.info(usage)
    logging.error("No valid command: >" + command + "<")
    exit()

rp = rospkg.RosPack()
fname = rp.get_path('dockeros') + '/config.yaml'
config = yaml.load(open(fname))
dock_obj = image.DockeROSImage(roscommand,
                               config=config)

commands["build"] = dock_obj.build_image
commands["run"] = dock_obj.run_image

if 1:
    commands[command]()
# except Exception as e:
#     logging.error("Failed to execute command")
#     logging.error(e)
#     raise e
#     exit()


# if not dock_obj.does_exist_on_client():
# else:
#     dock_obj.run_existing_image()
