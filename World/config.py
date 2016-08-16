import argparse
import sys
import pygame
from pygame.locals import *
from math import *
from libs.Helper import *
from libs.Point2 import *

# UDP communication defaults
LOCALHOST = "127.0.0.1"
INITIAL_PORT = 20000

# definition of kinds
UNKNOWN, BALL, POLE, ROBOT = "unkown", "ball", "pole", "robot"
# definition of sizes
OBJ_RADIUS = 7
ROBOT_RADIUS = 16

ROBOT_MAX_SPEED = 5
# how much velocity it keeps between cycles
FRICTION = 0.95

# window size
WIDTH = 800
HEIGHT = 600

FPS = 24

# keys for object creation
objectKeys = {
    K_o: UNKNOWN,
    K_b: BALL,
    K_p: POLE,
    K_r: ROBOT
}

# robot control keys
controlKeys = [K_RIGHT, K_LEFT, K_UP, K_DOWN, K_d, K_a]


# CAN'T TOUCH THIS! Parsing of arguments informed via command line
args_parser = argparse.ArgumentParser(
    description="This is the simulation of the world.")
args_parser.add_argument(
    "-d", "--debug", 
    help="Print debug messages", 
    action="store_true")
args_parser.add_argument(
    "address", 
    nargs="?",
    help="The IP address of the mind. Default is '127.0.0.1'",
    type=str, 
    default='127.0.0.1')
args = args_parser.parse_args()

config = {
    "debug": args.debug,
    "address": args.address or LOCALHOST
}



