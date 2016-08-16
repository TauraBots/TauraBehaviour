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

#Modifiable constants 
threshold = 0.15
radius = 15
memory_time = 10
increases_balldoubt = 10

# Starts the simulation and stores a reference to the robot you are controlling
robot = Simulation.start()

# Last ball seem informations
a_last_ball_seen = 0.0
p_last_ball_seen = pi/2
r_last_ball_seen = 0

# Doubt about ball
balldoubt = 0


# Memory for poles
a_last_pole1_seen = 0
r_last_pole1_seen = 0
a_last_pole2_seen = 0
r_last_pole2_seen = 0

# Defines if pole memories will be lost
poledoubt = 0

def look_around(direction):
    robot.setMovementVector( Point2(r=0, a=direction*(pi/2),phi=direction*(pi/2)) )


def walk_to(alpha, phi):
    robot.setMovementVector( Point2(r=1, a=alpha, phi=phi) )

  
def walk_side_left():
    robot.setMovementVector(Point2(r=1,a= pi/2,phi= 0))


def walk_side_right():
    robot.setMovementVector(Point2(r=1,a= -pi/2,phi= 0)) 


def stop_to_walk():
    robot.setMovementVector( Point2() )


def search_my_pole():
    for obj in world.objects_list:
        if obj.kind == "pole":
            if obj.position.r < 240: 
                return obj
    return None


def search_ball():
    for obj in world.objects_list:
        if obj.kind == "ball":
            return obj    
    return None


def focus_ball(ball_angle):
    robot.setMovementVector( Point2(r= 0, a=ball_angle, phi=ball_angle))


# def turn_head_to(direction):
#     robot.setNeck((hor,ver))

def search_my_goal():
    found = 0
    pole1 = None
    pole2 = None
    global r_last_pole2_seen
    global a_last_pole2_seen
    for obj in world.objects_list:
        if obj.kind == "pole":
            if obj.position.r < 220:
                found = found + 1
                if found == 1:
                    pole1 = obj
                    # If the object will be over +-pi/6 of last past position. It is the same pole1, else will be pole2
                    if pole1.position.a < a_last_pole1_seen - pi/6 or pole1.position.a > a_last_pole1_seen + pi/6:
                        r_last_pole2_seen = r_last_pole1_seen
                        a_last_pole2_seen = a_last_pole1_seen
                if found == 2:
                    pole2 = obj
    return pole1, pole2


def memorize_goal(pole1, pole2):
    global r_last_pole1_seen
    global a_last_pole1_seen
    global r_last_pole2_seen
    global a_last_pole2_seen
    global poledoubt 
    if pole1 and pole2 == None:
        r_last_pole1_seen = pole1.position.r
        a_last_pole1_seen = pole1.position.a
        poledoubt = 0
    if pole1 and pole2:
        r_last_pole1_seen = pole1.position.r
        a_last_pole1_seen = pole1.position.a
        r_last_pole2_seen = pole2.position.r
        a_last_pole2_seen = pole2.position.a        
        poledoubt = 0
    if pole1 == None and pole2 == None:
        poledoubt = poledoubt + 1
        # print(poledoubt)
        if poledoubt > memory_time:
            # Lost pole memories
            print("Poles memories are lost")
            r_last_pole1_seen = 0
            a_last_pole1_seen = 0
            r_last_pole2_seen = 0
            a_last_pole2_seen = 0
            poledoubt = 0
    



def memorize_ball(ball):
    global a_last_ball_seen
    global p_last_ball_seen
    global r_last_ball_seen
    global balldoubt
    a_last_ball_seen = ball.position.a
    p_last_ball_seen = ball.position.a
    r_last_ball_seen = ball.position.r
    balldoubt = 0

def stay_at_goal_center():

    return 1
    return 0

#direction =  1 L
#direction = -1 R
direction = 1
find = 0
closer_goal = 0
while robot.updateSimulation():
    world = robot.perceiveWorld()
    
    if not world:
        sys.exit("No world received")

    if not closer_goal:
        pole1,pole2 = search_my_goal()

        memorize_goal(pole1, pole2)

        if r_last_pole1_seen and not r_last_pole2_seen:
            walk_to(a_last_pole1_seen,a_last_pole1_seen)
            
        elif r_last_pole1_seen and r_last_pole2_seen:
            walk_to((a_last_pole1_seen+a_last_pole2_seen)/2,(a_last_pole1_seen+a_last_pole2_seen)/2)
            print(r_last_pole1_seen, r_last_pole2_seen)
            
        elif not pole2:
            look_around(direction)

        if  pole1 and not pole2:
            if pole1.position.r < 90:
                closer_goal = 1
                print(closer_goal)

    if closer_goal:
        poledoubt = poledoubt + 1
         
        ball = search_ball()

        if ball:
            focus_ball(ball.position.a)
            memorize_ball(ball)

        elif a_last_ball_seen and balldoubt < 10:
            focus_ball(a_last_ball_seen)
            balldoubt = balldoubt + 1

        else: 
            look_around(direction)


        if find == 0:
            pole1 = search_my_pole()
            if pole1:
                find = 1
                r_last_pole1_seen = pole1.position.r
                a_last_pole1_seen = pole1.position.a

                if pole1.position.a > 0:
                    direction = -1
                else: 
                    direction =  1
        elif find == 1:
            pole2 = search_my_pole()
            if pole2:
                find = 2
                r_last_pole2_seen = pole2.position.r
                a_last_pole2_seen = pole2.position.a
                
                if pole2.position.a > 0:
                    direction = -1
                else: 
                    direction =  1

        if find == 0 or find == 1: 
            look_around(direction)

        if find == 2:
            #se esta fora do centro do gol
            if r_last_pole1_seen > r_last_pole2_seen + 10 or r_last_pole1_seen < r_last_pole2_seen - 10:
                find = 0
                if a_last_pole1_seen > 0:
                    if r_last_pole1_seen > r_last_pole2_seen:
                        walk_side_left()
                    else:
                        walk_side_right()

                elif a_last_pole2_seen > 0:
                    if r_last_pole2_seen > r_last_pole1_seen:
                        walk_side_left()
                    else:
                        walk_side_right()                

        if poledoubt > 140:
            poledoubt = 0
            find = 0

        if pole1:
            if pole1.position.r > 90:
                closer_goal = 0

    time.sleep(1/10)