#########################################
#   TauraBots Player AI Version 0.9.4   #
#   Author: Fábiner de Melo Fugali      #
#   Date: 28/01/2016                    #
#########################################

from MindInterface import Simulation 
from MindInterface.config import *  

import time
from math import pi
from math import cos

# Modifiable constants 
THRESHOLD = 0.40
BALL_RADIUS = 14
BALL_MEMORY_CYCLE = 50
GOAL_MEMORY_CYCLE = 30
GOAL_LOOKING_CYCLE_MAX = 16
TILT_TO_LOOKING_GOAL = 5
THRESHOLD_TO_INTERCEPT = 60
THRESHOLD_ALIGN_BALL_TO_ROBOT = 0.015

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

robot1 = None

robot1_dist_ball = None

turn_to = 1

a_intercept = 0
direction = 0

# State 0
def ball_search():
    global ball
    object_search()
    if ball:
        do_measure()
        if robot1_dist_ball:
            if ball.position.r > robot1_dist_ball + THRESHOLD_TO_INTERCEPT:
                return 5
        return 1
    else:
        ball_look_around()
        return 0
  
# State 1
def ball_go_after():
    global ball_a_last_seen
    global ball_r_last_seen
    object_search()
    if ball_r_last_seen > BALL_RADIUS: 
        walk_to(ball_a_last_seen)
        return 1
    if ball_r_last_seen > 5:
        return 2
    else:
        return 0

# State 2
def opposite_goal_search():
    global pole1
    global pole2
    global balldoubt
    global goal_look_cycle
    object_search()
    if ball_doubt < BALL_MEMORY_CYCLE:
        if pole1 or pole2:
            return 3
        else:
            opposite_goal_look_around()
            return 2
    else: 
        goal_look_cycle = 0
        return 0

# State 3
def opposite_to_goal():
    global pole1
    global pole2
    object_search()
    if ball_doubt < BALL_MEMORY_CYCLE:
        if pole1 and pole2:
            if(pole1.position.a+pole2.position.a)/2>0-THRESHOLD/3 and (pole1.position.a+pole2.position.a)/2<0+THRESHOLD/3:
                return 4
            ball_turn_around()
        elif pole1:
            if pole1.position.a>0-THRESHOLD/3 and pole1.position.a<0+THRESHOLD/3:
                return 4
            ball_turn_around()
        else:
            return 2
        return 3
    else:
        return 0

# State 4
def kick():
    stop_to_walk()
    robot.updateSimulation()
    time.sleep(0.1)
    if ball_a_last_seen > 0:
        left_kick()
    else:
        right_kick()
    ball_free()
    robot.updateSimulation()
    time.sleep(0.1)
    return 0

# State 5
def ball_intercept():
    global ball_doubt
    global ball_a_last_seen
    global robot1
    global a_intercept
    global direction
    object_search()
    if robot1.position.a > ball_a_last_seen-THRESHOLD_ALIGN_BALL_TO_ROBOT and robot1.position.a < ball_a_last_seen+THRESHOLD_ALIGN_BALL_TO_ROBOT:
        direction = 0
        return 1
    if direction:
        walk_to(a_intercept)
        if direction > 4:
            a_intercept = 0
        direction+=1
    else: 
        do_direction()
        direction = 1
    if ball_doubt < BALL_MEMORY_CYCLE:
        return 5
    else:
        direction = 0 
        return 0

#def 

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
    robot_found = 0

    goal_doubt += GOAL_INCREASES_GOALDOUBT
    ball_doubt += BALL_INCREASES_BALLDOUBT
    for obj in world.objects_list:
        if obj.kind == "ball":
            if state == 0 or state == 1:
                ball = obj
                ball_memorize(ball)
        if obj.kind == "pole":
            pole_found +=1
            if pole_found == 1:
                pole1 = obj
            if pole_found == 2:
                pole2 = obj
            goal_memorize()
        if obj.kind == "robot":
            robot_found+=1
            if robot_found == 1:
                robot1 = obj
    
    if goal_doubt > GOAL_MEMORY_CYCLE:
        goal_free()
    if ball_doubt > BALL_MEMORY_CYCLE:
        ball_free()

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

# Subprocess 2
def turn_around():  
    global ball_look_cycle
    global ball_first_look 
    global turn_to
    robot.setMovementVector(Point2(r=0, a=turn_to,phi=turn_to))
    if  ball_look_cycle == 0:
        ball_first_look = 1
        stop_to_walk()
    else:
        ball_look_cycle -=1

# Subprocess 3
def walk_to(direction):
    robot.setMovementVector(Point2(r=1,a=direction,phi=direction))

# Subprocess 4
def stop_to_walk():
    robot.setMovementVector(Point2())

# Subprocess 5
def opposite_goal_look_around():
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
        ball_turn_around()

# Subprocess 6
def ball_turn_around():
    global turnto
    robot.setMovementVector(Point2(r=1, a=pi/2*turn_to,phi=-pi/2*turn_to))

# Subprocess 7
def left_kick():
    robot.setKick( 1)

# Subprocess 8
def right_kick():
    robot.setKick(-1)

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

# Subprocess 12
def do_measure():
    global robot1
    global robot1_dist_ball

    if robot1:
        a = robot1.position.a
        b = robot1.position.r
        c = ball_r_last_seen
        robot1_dist_ball = sqrt(b*b+c*c-2*b*c*cos(a))
    else:
        robot1_dist_ball = None

# Subprocess 13
def do_direction():
    global a_intercept
    global robot1
    global robot1_dist_ball
    if robot1.position.a > ball_r_last_seen:
        a_intercept = -1.5*abs(robot1.position.a)
    else:
        a_intercept =  1.5*abs(robot1.position.a)   

#D= dist robot to ball
#d = robo.r
#beta = a ball - a robot
#gama = direcao
#Gama = arcsen( (d/D) * sen("beta") ) - 90[graus];

#ball_search, ball_go_after, goal_search, self_opposite_to_goal, kick = range(5)

# States
def switch(state):
    if   state == 0: state = ball_search() 
    elif state == 1: state = ball_go_after()
    elif state == 2: state = opposite_goal_search()
    elif state == 3: state = opposite_to_goal()
    elif state == 4: state = kick()
    elif state == 5: state = ball_intercept()
    else:
        print("ERROR!")
    return state
    
INITIAL_STATE = 0
state = INITIAL_STATE

robot = Simulation.start()

while robot.updateSimulation():
    world = robot.perceiveWorld()
    robot.setKick(0)  
    if not world:
        sys.exit("No world received")
    state = switch(state)
    # debug
    #print("ball_look_cycle = ", ball_look_cycle)
    #print("goal_look_cycle = ", goal_look_cycle)
    print("state = ", state)
    #print("pan = ", pan)
    #print("tilt = ", tilt)
    #print("ball_doubt = ", ball_doubt)
    #print("goal_doubt = ", goal_doubt)
    #print("turn_to = ", turn_to)
    print("robot1_dist_ball = ",robot1_dist_ball)
    print("ball_r_last_seen = ",ball_r_last_seen)
    #print("ball_a_last_seen = ",ball_a_last_seen)
    #if robot1:
    #    print("robot1.a = ", robot1.position.a)
    #print("a_intercept = ", a_intercept)
    print("===================")
    time.sleep(0.1)