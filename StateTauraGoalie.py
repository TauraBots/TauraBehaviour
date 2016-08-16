#########################################
#   TauraBots Goalie AI Version 0.3.0   #
#   Author: Fábiner de Melo Fugali      #
#   Date: 29/10/2015                    #
#########################################

from MindInterface import Simulation 
from MindInterface.config import *  

import time
from math import pi

#import TauraGameController
#import threading

#from random import random

# Modifiable constants
THRESHOLD = 0.40
BALL_RADIUS = 14
BALL_MEMORY_CYCLE = 50
GOAL_MEMORY_CYCLE = 30
GOAL_LOOKING_CYCLE_MAX = 16
TILT_TO_LOOKING_GOAL = 5
#THRESHOLD_TO_INTERCEPT = 60
#THRESHOLD_ALIGN_BALL_TO_ROBOT = 0.015

# Constants
TILT_MAX  =  30 * pi/180
TILT_MIN  = -90 * pi/180
TILT_STEP =  40 * pi/180
PAN_MAX   =  100 * pi/180
PAN_MIN   = -100 * pi/180
PAN_STEP  =  25 * pi/180
BALL_INCREASES_BALLDOUBT = 1
GOAL_INCREASES_GOALDOUBT = 1

pan  = PAN_MIN
tilt = TILT_MIN

increasing_pan = 1

# Ball Memories
ball_a_last_seen = 0
ball_r_last_seen = 0
ball_doubt = BALL_MEMORY_CYCLE
ball_look_cycle = 0

ball_first_look = 1

# Goal Memories
pole1_a_last_seen = 0
pole1_r_last_seen = 0
pole2_a_last_seen = 0
pole2_r_last_seen = 0
goal_doubt = GOAL_MEMORY_CYCLE
goal_look_cycle = 0

ball  = None
pole1 = None
pole2 = None

turn_to = -1

pole_found = 0

#0
def home_goal_search():
    global pole1
    global pole2
    global balldoubt
    global goal_look_cycle
    object_search()
    if pole1:
        return 1
    else:
        home_goal_look_around()
        return 0

# State 1
def goal_go_after():
    global pole1_a_last_seen
    global pole1_r_last_seen
    global pole2_a_last_seen
    global pole2_r_last_seen

    object_search()
    if goal_doubt < GOAL_MEMORY_CYCLE/2:
        if pole1_r_last_seen and pole2_r_last_seen:
            if (pole1_r_last_seen + pole2_r_last_seen)/2 > 70:
                walk_to((pole1_a_last_seen+pole2_a_last_seen)/2)
                return 1
        if pole1_r_last_seen and not pole2_r_last_seen:
            if pole1_r_last_seen > 70:
                walk_to(pole1_a_last_seen)
                return 1
        return 2 #goal central
    else:
        return 0

#State 2
def goal_center():
    pole_search()
    if goal_doubt < GOAL_MEMORY_CYCLE:
        if pole1_r_last_seen > pole2_r_last_seen + 10 or pole1_r_last_seen < pole2_r_last_seen - 10:
            if pole1_r_last_seen > 0:
                if pole1_r_last_seen > pole2_r_last_seen:
                    walk_side_left()
                else:
                    walk_side_right()
            elif pole2_r_last_seen > 0:
                if pole2_r_last_seen > pole1_r_last_seen:
                    walk_side_left()
                else:
                    walk_side_right()
            return 2
        else:
            return 3
    else:
        return 0
#State 3
def ball_search():
    global ball
    object_search()
    if goal_doubt < GOAL_MEMORY_CYCLE:
        if ball:
            return 4
        else:
            ball_look_around()
            return 3
    else:
        return 0

#State 4
def focus_ball():
    global ball_a_last_seen
    object_search()
    if goal_doubt < GOAL_MEMORY_CYCLE:
        if ball_r_last_seen > 200:
            robot.setMovementVector( Point2(r= 0, a=ball_a_last_seen, phi=ball_a_last_seen))
            return 4
        else:
            return 5#se atira na bola
    else:
        return 0

#State 5
def goalie_action():
    object_search()
    if goal_doubt < GOAL_MEMORY_CYCLE:
        if ball_a_last_seen > 0:
            print("defende para a esquerda")
        else:
            print("defende para a direita")
    return 0

def pole_search():
    global pole_found
    global pole1
    global pole2

    if pole_found == 0:
        pole1 = None
        pole2 = None

    for obj in world.objects_list:
        if obj.kind == "pole":
            pole_found +=1
            if pole_found == 1:
                if obj.position.r < 240:
                    pole1 = obj
            if pole_found == 2:
                if obj.position.r < 240:
                    pole2 = obj
                pole_found = 0
            home_goal_memorize()


def look_around(direction):
    robot.setMovementVector( Point2(r=0, a=direction*(pi/2),phi=direction*(pi/2)) )


  
def walk_side_left():
    robot.setMovementVector(Point2(r=1,a= pi/2,phi= 0))


def walk_side_right():
    robot.setMovementVector(Point2(r=1,a= -pi/2,phi= 0)) 


def stop_to_walk():
    robot.setMovementVector( Point2() )


# Subprocess 9
def ball_memorize(ball):
    global ball_a_last_seen
    global ball_r_last_seen
    global ball_doubt
    global ball_first_look
    global ball_look_cycle
    ball_a_last_seen = ball.position.a
    ball_r_last_seen = ball.position.r
    ball_doubt = 0
    ball_first_look = 1
    ball_look_cycle = 0
   
# Subprocess 10
def ball_free():
    global ball
    global ball_a_last_seen
    global ball_r_last_seen
    global ball_doubt
    ball_a_last_seen = 0
    ball_r_last_seen = 0
    ball_doubt = BALL_MEMORY_CYCLE
    ball = None


# Subprocess x
def home_goal_look_around():
    global increasing_pan
    global pan
    global PAN_MIN
    global PAN_MAX
    global PAN_STEP
    global goal_look_cycle
    if goal_look_cycle <= GOAL_LOOKING_CYCLE_MAX :
        if pan < PAN_MAX and increasing_pan == 1:
            pan += PAN_STEP
        elif pan > PAN_MIN and increasing_pan == 0:
            pan -= PAN_STEP
        else:
            increasing_pan = not increasing_pan
        robot.setNeck((pan,TILT_TO_LOOKING_GOAL))
        goal_look_cycle+=1

    else:
        turn_around()

# Subprocess 2
def turn_around():
    global turn_to
    robot.setMovementVector(Point2(r=0, a=turn_to,phi=turn_to))

# Subprocess 11
def goal_memorize():
    global pole1_a_last_seen
    global pole1_r_last_seen
    global pole2_a_last_seen
    global pole2_r_last_seen
    global goal_doubt
    global goal_look_cycle
    global turn_to
    global pole1
    global pole2
    goal_look_cycle = 0
    pole1_a_last_seen = pole1.position.a
    pole1_r_last_seen = pole1.position.r
    goal_doubt = 0
    if pole2:
        pole2_a_last_seen = pole2.position.a
        pole2_r_last_seen = pole2.position.r
        if ball_doubt < BALL_MEMORY_CYCLE:
            if(pole1_a_last_seen + pole2_a_last_seen)/2 < 0:
                turn_to =  1
            else:
                turn_to = -1
    elif ball_doubt < BALL_MEMORY_CYCLE:
        if pole1_a_last_seen < 0:
            turn_to =  1
        else:
            turn_to = -1

# Subprocess 12
def goal_free():
    global pole1
    global pole2
    global pole1_a_last_seen
    global pole1_r_last_seen
    global pole2_a_last_seen
    global pole2_r_last_seen
    global goal_doubt
    pole1_a_last_seen = 0
    pole1_r_last_seen = 0
    pole2_a_last_seen = 0
    pole2_r_last_seen = 0
    goal_doubt = GOAL_MEMORY_CYCLE
    pole1 = None
    pole2 = None

def memorize_ball(ball):
    global a_last_ball_seen
    global p_last_ball_seen
    global r_last_ball_seen
    global balldoubt
    a_last_ball_seen = ball.position.a
    p_last_ball_seen = ball.position.a
    r_last_ball_seen = ball.position.r
    balldoubt = 0

# Subprocess 0
def object_search():
    global state

    global ball_doubt
    global goal_doubt
    global ball
    global pole1
    global pole2
    global robot1
    pole_found  = 0

    goal_doubt += GOAL_INCREASES_GOALDOUBT
    ball_doubt += BALL_INCREASES_BALLDOUBT
    for obj in world.objects_list:
        if obj.kind == "ball":
            ball = obj
            ball_memorize(ball)
        if obj.kind == "pole":
            pole_found +=1
            if pole_found == 1:
                pole1 = obj
            if pole_found == 2:
                pole2 = obj
            goal_memorize()

    if goal_doubt > GOAL_MEMORY_CYCLE:
        goal_free()
    if ball_doubt > BALL_MEMORY_CYCLE:
        ball_free()

# Subprocess 10
def ball_free():
    global ball
    global ball_a_last_seen
    global ball_r_last_seen
    global ball_doubt
    ball_a_last_seen = 0
    ball_r_last_seen = 0
    ball_doubt = BALL_MEMORY_CYCLE
    ball = None

# Subprocess 12
def goal_free():
    global pole1
    global pole2
    global pole1_a_last_seen
    global pole1_r_last_seen
    global pole2_a_last_seen
    global pole2_r_last_seen
    global goal_doubt
    pole1_a_last_seen = 0
    pole1_r_last_seen = 0
    pole2_a_last_seen = 0
    pole2_r_last_seen = 0
    goal_doubt = GOAL_MEMORY_CYCLE
    pole1 = None
    pole2 = None

    # Subprocess 11
def goal_memorize():
    global pole1_a_last_seen
    global pole1_r_last_seen
    global pole2_a_last_seen
    global pole2_r_last_seen
    global goal_doubt
    global goal_look_cycle
    global turn_to
    global pole1
    global pole2
    goal_look_cycle = 0
    pole1_a_last_seen = pole1.position.a
    pole1_r_last_seen = pole1.position.r
    goal_doubt = 0
    if pole2:
        pole2_a_last_seen = pole2.position.a
        pole2_r_last_seen = pole2.position.r
        if ball_doubt < BALL_MEMORY_CYCLE:
            if(pole1_a_last_seen + pole2_a_last_seen)/2 < 0:
                turn_to =  1
            else:
                turn_to = -1
    elif ball_doubt < BALL_MEMORY_CYCLE:
        if pole1_a_last_seen < 0:
            turn_to =  1
        else:
            turn_to = -1

# Subprocess 1
def ball_look_around():
    global ball_first_look
    global increasing_pan
    global pan
    global tilt
    global TILT_MIN
    global TILT_MAX
    global PAN_MIN
    global PAN_MAX
    global TILT_STEP
    global PAN_STEP
    global ball_look_cycle
    robot.setNeck((pan,tilt))
    if ball_first_look == 1:
        ball_first_look = 0
        pan = PAN_MIN
        tilt = TILT_MIN
        increasing_pan = 1
        ball_look_cycle = 0
    if(tilt <= TILT_MAX):
        ball_look_cycle +=1
        if pan < PAN_MAX and increasing_pan == 1:
            pan += PAN_STEP
        elif pan > PAN_MIN and increasing_pan == 0:
            pan -= PAN_STEP
        else:
            tilt += TILT_STEP
            increasing_pan = not increasing_pan           
    else:
        robot.setNeck((0,0))
        turn_around()

# Subprocess 3
def walk_to(direction):
    robot.setMovementVector(Point2(r=1,a=direction,phi=direction))

def switch(state):
    if   state == 0: state = search_home_goal()
    elif state == 1: state = goal_go_after()
    elif state == 2: state = goal_center()
    elif state == 3: state = ball_search()
    elif state == 4: state = focus_ball()
    elif state == 5: state = action()
    else: print("ERROR!")
    return state

INITIAL_STATE = 0
state = INITIAL_STATE

robot = Simulation.start()

while robot.updateSimulation():
    world = robot.perceiveWorld()
    if not world:
        sys.exit("No world received")

    state = switch(state)
    print("state = ", state)
    print("goal_doubt = ", goal_doubt)

    print("===================")
    time.sleep(0.3)