import argparse
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


def ip_validator(input):
    ip_and_port = input.split(":")
    if len(ip_and_port) != 2:
        msg = "Please give host in the format host:port, e.g. 10.3.4.1:2375 or hostname:2375"
        raise argparse.ArgumentTypeError(msg)
    return input


parser = argparse.ArgumentParser(
    prog="dockeros",
    description="Simply running ros nodes in docker containers on remote robots.")
parser.add_argument("subcommand", choices=["build", "run", "stop", "push"],
    help="build: Creates an image that can run roscommand\n\
run: Runs an image with your_roscommand (and builds it first)\n\
stop: Stops image that runs that command\n\
push: Push image to predefined registry\n")

g = parser.add_mutually_exclusive_group()
g.add_argument("-e", "--env", action='store_true', default=True,
    help="Use the existing docker environment (e.g. DOCKER_HOST)")
g.add_argument("-i", "--ip", "--host", nargs=1, type=ip_validator, metavar='HOST:PORT',
    help="Set the host to deploy image to")

parser.add_argument("-f", "--dockerfile", nargs=1, type=str,
    help="Use a custom Dockerfile")
parser.add_argument("-n","--no-build", action='store_true',
    help="Dont (re-)build the image before running")

parser.add_argument("roscommand", nargs=argparse.REMAINDER,
    help="Everything after the subcommand will be interpreted as the ros command to be run in your image")

args = parser.parse_args()
print(args)
print(args.subcommand)

def dummy():
    logging.info("to be implemented ..")

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

if command == "build":
    dock_obj.build_image()

if command == "run":
    dock_obj.run_image(ip, port)
