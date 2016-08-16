from MindInterface import Simulation 
from MindInterface.config import *  

import time
from math import pi


robot = Simulation.start()

def search_ball():
    for obj in world.objects_list:
        if obj.kind == "ball":
            return obj    
    return None

while robot.updateSimulation():
    world = robot.perceiveWorld()
        
    if not world:
        sys.exit("No world received")

    ball = search_ball()
    if ball:
    	print(ball.position.r)
    else:
    	print ("NADA")
    time.sleep(0.1)