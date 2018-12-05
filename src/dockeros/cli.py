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

parser = argparse.ArgumentParser(
    prog="dockeros",
    description="Simply running ros nodes in docker containers on remote robots.")
parser.add_argument("subcommand", choices=["build", "run", "stop", "push"],
    help="build: Creates an image that can run roscommand\n\
run: Runs an image with your_roscommand (and builds it first)\n\
stop: Stops image that runs that command\n\
push: Push image to predefined registry\n")
parser.add_argument("-f", "--dockerfile", nargs=1, type=str,
    help="Use a custom Dockerfile")
parser.add_argument("roscommand", nargs=argparse.REMAINDER,
    help="Everything after the subcommand will be interpreted as the ros command to be run in your image")

args = parser.parse_args()
print(args)

usage = "USAGE:\n" + \
        "," * 80 + "\n" \
        "For examle:\n" \
        "$ dockeros run -h 10.3.1.120:2375 roslaunch ros_naviagtion move_base.launch\n" \
        "Will perform the ros command in a docker container at the mentioned IP\n" + \
        "\n" \
        "Reference:\n" \
        "$ dockeros <subcommand> <options> <your_roscommand>\n" \
        "\n" \
        "Subcommands:\n" \
        " build <your_roscommand>\n\tCreates an image that can run your_roscommand\n" \
        " run <your_roscommand>\n\tRuns an image with your_roscommand (and builds it first)\n" \
        "\n" \
        "Options:\n" \
        " -f, --dockerfile <path>\n\tUse a custom Dockerfile\n" \
        " -e, --env\n\tUse the set docker environment (e.g. DOCKER_HOST)\n" \
        " -h, --host <ip:port>\n\tSet the host to deploy image to\n" \
        " -n, --no-build\n\tDont (re-)build the image before running\n" \
        "'" * 80 + "\n" \

# def dummy():
#     logging.info("to be implemented ..")
#
# try:
#     command = sys.argv[1]
# except:
#     logging.info(usage)
#     exit()
#
# if command == "_get_allowed_roscommands":
#     print(" ".join(image._get_allowed_roscommands()))
#     exit()
# elif command == "build" or command == "push":  # no ip needed
#     try:
#         roscommand = sys.argv[2:]
#         ip = ""
#         port = ""
#     except:
#         logging.info(usage)
#         logging.error("Ros command not entered! exiting script")
#         exit()
# elif command == "run":  # ip needed
#     try:
#         ip_and_port = sys.argv[2]
#         ip = ip_and_port.split(':')[0]
#         port = ip_and_port.split(':')[1]
#     except:
#         logging.info(usage)
#         logging.error("Host and/or port not entered! exiting script")
#         exit()
#
#     try:
#         roscommand = sys.argv[3:]
#     except:
#         logging.info(usage)
#         logging.error("Ros command not entered! exiting script")
#         exit()
# else:
#     logging.info(usage)
#     logging.error("No valid command: >" + command + "<")
#     exit()
#
# rp = rospkg.RosPack()
# fname = rp.get_path('dockeros') + '/config.yaml'
# config = yaml.load(open(fname))
# dock_obj = image.DockeROSImage(roscommand,
#                                config=config)
#
# if command == "build":
#     dock_obj.build_image()
#
# if command == "run":
#     dock_obj.run_image(ip, port)
