from MindInterface.config import *
import sys
from MindInterface.Controller import *

######################################

robot_controller = None

def start():
    return Controller(config['index'])

def brainless_start():
    robot_controller = Controller(config['index'])
    play = True
    while play:
        play = robot_controller.updateSimulation()

