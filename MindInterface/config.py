import argparse
from libs.Helper import *
import sys

# UDP communication defaults
LOCALHOST = "127.0.0.1"
#LOCALHOST = "192.168.1.122"
INITIAL_PORT = 20000

# definition of kinds
UNKNOWN, BALL, POLE, ROBOT = "unkown", "ball", "pole", "robot"
# definition of sizes
OBJ_RADIUS = 10
ROBOT_RADIUS = 10


# CAN'T TOUCH THIS! Parsing of arguments informed via command line
args_parser = argparse.ArgumentParser(description='This is the interface to control the robot.')
args_parser.add_argument(
    "index",
    nargs="?",
    help="The id of the robot. 1st robot added to the simulation is 0, 2nd is 1 and so on. Default is 0.",
    type=int,
    default=0)
args_parser.add_argument(
    "address",
    nargs="?",
    help="The IP address of the body, simulated (WorldSimulation) or not. Default is '127.0.0.1'.",
    type=str,
    default='127.0.0.1')
args_parser.add_argument(
    "-g", "--graphics",
    help="Uses the GUI and pygame",
    action="store_true")
args_parser.add_argument(
    "-d", "--debug", 
    help="Print debug messages", 
    action="store_true")
args = args_parser.parse_args()

config = {
    "index": args.index or 0,
    "address": args.address or LOCALHOST,
    "gui": args.graphics,
    "debug": args.debug
}
