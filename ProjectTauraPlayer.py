#########################################
#   TauraBots Player AI Version 0.9.0   #
#   Author: Fábiner de Melo Fugali      #
#   Date: 31/10/2015                    #
#########################################

from MindInterface import Simulation 
from MindInterface.config import *  

import time
from math import pi

#Modifiable constants 
THRESHOLD = 0.40
BALL_RADIUS = 10
BALL_MEMORY_CYCLE = 60
POLE_MEMORY_CYCLE = 20
BALL_INCREASES_BALLDOUBT = 1
POLE_INCREASES_POLEDOUBT = 1

# Starts the simulation and stores a reference to the robot you are controlling
robot = Simulation.start()

# Starts by default to turn around ball anticlockwise
turnto = 1

#Constants
TILT_MAX  =  30 * pi/180
TILT_MIN  = -90 * pi/180
TILT_STEP =  40 * pi/180
PAN_MAX   =  100 * pi/180
PAN_MIN   = -100 * pi/180
PAN_STEP  =  25 * pi/180

pan  = PAN_MIN
tilt = TILT_MIN

increasing_pan = 1

# Memória da Bola
ball_a_last_seen = 0
ball_r_last_seen = 0
ball_doubt = 0
ball_closer = 0

# Mémoria do Poste
pole_doubt = 0

flag = 0
cycle_count = 0

ball_first_look = 1
increasing_pan = 1

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
    global cycle_count
    global flag

    if ball_first_look:
        ball_first_look = 0
        pan = PAN_MIN
        tilt = TILT_MIN
        increasing_pan = 1
        cycle_count = 0

    if(tilt <= TILT_MAX):
        robot.setNeck((pan,tilt))
        cycle_count = cycle_count + 1

        if pan < PAN_MAX and increasing_pan == 1:
            pan += PAN_STEP
        elif pan > PAN_MIN and increasing_pan == 0:
            pan -= PAN_STEP
        else:
            tilt += TILT_STEP
            increasing_pan = not increasing_pan    
    else:
        robot.setNeck((0,0))
        flag = 1

def self_turn_around():  
    global cycle_count 
    global flag
    global ball_first_look 

    #definir a quantidades de ciclos necessárias para girar exatamente a quantidade de ângulos no campo.
    #exemplo: girar 90 graus a quantidade de ciclos deve ser 100
    robot.setMovementVector( Point2(r=0, a=turnto,phi=turnto) )
    if  cycle_count == 0:
        flag = 0 
        ball_first_look = 1
    else:
        cycle_count = cycle_count - 1
        
def goal_look_arround():
    global increasing_pan
    global pan
    global PAN_MIN
    global PAN_MAX
    global PAN_STEP

    if pan < PAN_MAX and increasing_pan == 1:
        pan += PAN_STEP
    elif pan > PAN_MIN and increasing_pan == 0:
        pan -= PAN_STEP
    else:
        increasing_pan = not increasing_pan
    robot.setNeck((pan,10))

def self_walk_to(r, alpha, phi):
    robot.setMovementVector( Point2(r=1, a=alpha, phi=phi) )
 
def self_stop_to_walk():
    robot.setMovementVector( Point2() )

def ball_turn_around(t):
    robot.setMovementVector( Point2(r=1, a=pi/2*t,phi=-pi/2*t) )

def self_left_kick():
    robot.setKick( 1)

def self_right_kick():
    robot.setKick(-1)

def ball_search():
    for obj in world.objects_list:
        if obj.kind == "ball":
            return obj    
    return None

def goal_search():
    found = 0
    pole1 = None
    pole2 = None
    for obj in world.objects_list:
        if obj.kind == "pole":
            found = found + 1
            if found == 1:
                pole1 = obj
                
            if found == 2:
                pole2 = obj
    return pole1, pole2

def ball_go_after():
    global ball_r_last_seen
    global ball_a_last_seen

    if ball_r_last_seen > BALL_RADIUS: 
        self_walk_to(1, ball_a_last_seen, ball_a_last_seen)
        return 0
    #soluciona o problema da tangente
    elif ball_r_last_seen > 5:
        return 1

def self_opposite_to_goal(pole1, pole2):
    if pole1 and pole2:
        if(pole1.position.a + pole2.position.a)/2 > 0 - THRESHOLD/ 3 and (pole1.position.a + pole2.position.a)/2 < 0 + THRESHOLD / 3:
            return 1
        if(((pole1.position.a + pole2.position.a)/2) < 0):
            ball_turn_around( 1)
        else:
            ball_turn_around(-1)
        
    elif pole1:
        if pole1.position.a > 0 - THRESHOLD / 3 and pole1.position.a < 0 + THRESHOLD / 3:
            return 1
        if pole1.position.a < 0:
            ball_turn_around( 1)
        else:
            ball_turn_around(-1)
    else:
        return 0

def ball_memorize(ball):
    global ball_a_last_seen
    global ball_r_last_seen
    global ball_doubt
    global ball_first_look
    global flag
    global cycle_count

    ball_a_last_seen = ball.position.a
    ball_r_last_seen = ball.position.r
    ball_doubt = 0
    ball_first_look = 1
    cycle_count = 0

    flag = 0


def ball_free():
    global ball_a_last_seen
    global ball_r_last_seen
    global ball_doubt
    ball_a_last_seen = 0
    ball_r_last_seen = 0
    ball_doubt = 0


while robot.updateSimulation():
    world = robot.perceiveWorld()
    robot.setKick(0)
        
    if not world:
        sys.exit("No world received")

    ball = ball_search()

    if ball_closer:
        pole1, pole2 = goal_search()
        if(self_opposite_to_goal(pole1, pole2)):
            self_stop_to_walk()
            robot.updateSimulation()
            time.sleep(0.1)
            if ball_a_last_seen > 0:
                self_left_kick()
            else:
                self_right_kick()
            ball_free()
            ball_closer = 0
            robot.updateSimulation()
            time.sleep(0.1)

        else:
            goal_look_arround()
            pole_doubt+=POLE_INCREASES_POLEDOUBT
            if pole_doubt > POLE_MEMORY_CYCLE:
                self_stop_to_walk()
                robot.updateSimulation()
                time.sleep(0.1)
                
                if ball_a_last_seen > 0:
                    self_left_kick()
                else:
                    self_right_kick()
                ball_free()
                ball_closer = 0
                robot.updateSimulation()
                time.sleep(0.1)
                pole_doubt = 0
        
    elif ball:
        print("atual ball radius = ", ball.position.r)
        print("last ball_radius = ",ball_r_last_seen)    
        ball_memorize(ball)
        ball_closer = ball_go_after()
        if ball_a_last_seen > 0:
            turnto =  1
        else:
            turnto = -1
    
    #se não tem a bola e tem memória da bola    
    elif not ball and ball_r_last_seen:

        ball_closer = ball_go_after()
        ball_doubt += BALL_INCREASES_BALLDOUBT
    
    #se não tem memória e nem bola
    else: 
        self_stop_to_walk()

        if flag:
            self_turn_around()
        else:

            ball_look_around()
            
        ball_doubt += BALL_INCREASES_BALLDOUBT

    if ball_doubt > BALL_MEMORY_CYCLE:
        ball_free()

    #if config["debug"]:
    #print("ball_doubt = ",ball_doubt)
    #print("pole_doubt = ",pole_doubt)
    #print("ball_closer = ",ball_closer)
   
    
    print("cycle_count = ",cycle_count)
    print("flag = ", flag)
    print("pan = ", pan)
    print("tilt = ", tilt)
        
    
    print("===========")
    time.sleep(0.1)