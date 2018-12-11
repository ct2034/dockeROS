import argparse
from argparse import RawTextHelpFormatter
import sys
import image
import logging
import yaml
import os
import rospkg

logging.getLogger().setLevel(logging.INFO)

def ip_validator(input):
    ip_and_port = input.split(":")
    if len(ip_and_port) != 2:
        msg = "Please give host in the format host:port, e.g. 10.3.4.1:2375 or hostname:2375"
        raise argparse.ArgumentTypeError(msg)
    return ip_and_port


parser = argparse.ArgumentParser(
    prog="dockeros",
    formatter_class=RawTextHelpFormatter,
    description="Simply running ros nodes in docker containers on remote robots.")
parser.add_argument("subcommand", choices=["build", "run", "stop", "push"],
    help="build: Creates an image that can run roscommand\n\
run: Runs an image with your_roscommand (and builds it first)\n\
stop: Stops image that runs that command\n\
push: Push image to predefined registry\n")

g = parser.add_mutually_exclusive_group()
g.add_argument("-e", "--env", action='store_true', default=True,
    help="use the existing docker environment (see https://dockr.ly/2zMPc17 for details)")
g.add_argument("-i", "--ip", "--host", nargs=1, type=ip_validator, metavar='HOST:PORT',
    help="set the host (robot) to deploy image to")

parser.add_argument("-f", "--dockerfile", nargs=1, type=open, default=None,
    help="use a custom Dockerfile")
parser.add_argument("-n","--no-build", action='store_true',
    help="dont (re-)build the image before running")

parser.add_argument("roscommand", nargs=argparse.REMAINDER,
    help="Everything after the subcommand will be interpreted as the ros command to be run in your image")


args = parser.parse_args()
if args.dockerfile:
    dockerfname = os.path.realpath(args.dockerfile[0].name)
    args.dockerfile[0].close()
    logging.debug(dockerfname)
else:
    dockerfname = False
logging.debug(args)

rp = rospkg.RosPack()
fname = rp.get_path('dockeros') + '/config/config.yaml'
try:
    config = yaml.load(open(fname))
except Exception as e:
    logging.warn("No config file found under " + fname)
    config = {}
dock_obj = image.DockeROSImage(args.roscommand,
                               config=config,
                               dockerfile=dockerfname)
if args.env:
    dock_obj.make_client()
else:
    dock_obj.make_client(args.ip_and_port[0], args.ip_and_port[1])

if args.subcommand == "build":
    dock_obj.build()

elif args.subcommand == "run":
    if not args.no_build:
        dock_obj.build()
    dock_obj.run()

elif args.subcommand == "stop":
    dock_obj.stop()

elif args.subcommand == "push":
    dock_obj.push()
