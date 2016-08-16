#######################################
#   TauraBots AI Version 0.2.0        #
#   Author: Fábiner de Melo Fugali    #
#   Date: 19/10/2015                  #
#######################################


from MindInterface import Simulation 
from MindInterface.config import *  

import time
from math import pi

import TauraGameController
import threading

#from random import random

#Modifiable constants 
threshold = 0.05
radius = 15
memory_time = 30
increases_balldoubt = 10

# Starts the simulation and stores a reference to the robot you are controlling
robot = Simulation.start()

# Last ball seem informations
a_last_ball_seen = 0.0
p_last_ball_seen = pi/2
r_last_ball_seen = 0

# Doubt about ball
balldoubt = 0

# Starts by default to turn around ball anticlockwise
turnto = 1

# Memory for poles
a_last_pole1_seen = 0
r_last_pole1_seen = 0
a_last_pole2_seen = 0
r_last_pole2_seen = 0

# Defines if pole memories will be lost
poledoubt = 0

# Last object position is blocking me
a_last_obstacle_position = 0


#trend = 0


def look_around():
    robot.setMovementVector( Point2(r=0, a=a_last_ball_seen,phi=p_last_ball_seen) )


def avoid_by_left():
    robot.setMovementVector(Point2(r=1,a= pi/2,phi= pi/2)) 


def avoid_by_right():
    robot.setMovementVector(Point2(r=1,a= -pi/2,phi= pi/2))


def walk_to(alpha, phi):
    robot.setMovementVector( Point2(r=1, a=alpha, phi=phi) )

  
def walk_side_left():
    robot.setMovementVector(Point2(r=1,a= pi/2,phi= 0))


def walk_side_right():
    robot.setMovementVector(Point2(r=1,a= -pi/2,phi= 0)) 


def stop_to_walk():
    robot.setMovementVector( Point2() )


def turn_around_ball(t):
    robot.setMovementVector( Point2(r=1, a=pi/2*t,phi=-pi/2*t) )


def search_pole():
    robot.setMovementVector( Point2(r=1, a=-pi/2 * turnto, phi=pi/2 * turnto) )


def left_kick():
    robot.setKick( 1)


def right_kick():
    robot.setKick(-1)


def search_ball():
    for obj in world.objects_list:
        if obj.kind == "ball":
            return obj    
    return None


def search_goal():
    found = 0
    pole1 = None
    pole2 = None
    global r_last_pole2_seen
    global a_last_pole2_seen
    for obj in world.objects_list:
        if obj.kind == "pole":
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


def go_after_ball(ball):
    global a_last_obstacle_position
    # If ball is far or lost align to ball
    if ball.position.r > radius or (ball.position.a < -threshold or ball.position.a > threshold):
        obstacle = obstacle_detection(ball) 
        if obstacle:
            obstacle_avoidance(obstacle)
            a_last_obstacle_position = obstacle.position.a 
        else:
            walk_to(ball.position.a, ball.position.a)
     
        # Verify if I can move myself to direction of ball
        if r_last_ball_seen > ball.position.r-threshold and r_last_ball_seen < ball.position.r+threshold and ball.position.r > radius:
            print("I can't move!")
            if a_last_obstacle_position < 0:
                walk_side_left()
            if a_last_obstacle_position > 0:
                walk_side_right()    
        return 0
    else:
        return 1


def obstacle_detection(ball):
    for obj in world.objects_list:
        # If some object is obstacle
        if obj.position.a > ball.position.a -pi/2 and obj.position.a < ball.position.a + pi/2 and ball.position.r > radius and obj.kind != "ball" and obj.position.r < ball.position.r and obj.position.r < radius:
            print("there is a obstacle")
            return obj
    return None


def obstacle_avoidance(obs):
    if obs.position.a < 0:
        print("avoid by left")
        avoid_by_left()        
    else:
        print("avoid by right")
        avoid_by_right()
      

def opposite_to_goal_center(pole1, pole2):
    if pole1 and pole2:
        if(((pole1.position.a + pole2.position.a)/2) < 0):
            # Anticlockwise
            turn_around_ball( 1)
        else:
            # Clockwise
            turn_around_ball(-1)
    elif pole1:
        if (pole1.position.a + a_last_pole2_seen)/2 < 0:
            # Anticlockwise
            turn_around_ball( 1)
        else:
            # Clockwise
            turn_around_ball(-1)


def kick(pole1, pole2, ball):
    if pole1 and pole2 and ball:
        if try_kick(pole1.position.a, pole2.position.a):
            print("kick")
            if ball.position.a > 0:
                left_kick()
            else:
                right_kick()
    elif pole1 and ball: 
        a_last_position2 = a_last_pole2_seen
        if try_kick(pole1.position.a, a_last_position2):
            print("kick")
            if ball.position.a > 0:
                left_kick()
            else:
                right_kick()
  
    elif pole1 == None:
        # Turn around ball 
        search_pole()


def try_kick(position1, position2):
    if((position1 + position2)/2 > -threshold and (position1 + position2)/2 < threshold):
        return 1
    else:
        return 0


def memorize_ball(ball):
    global a_last_ball_seen
    global p_last_ball_seen
    global r_last_ball_seen
    global balldoubt
    a_last_ball_seen = ball.position.a
    p_last_ball_seen = ball.position.a
    r_last_ball_seen = ball.position.r
    balldoubt = 0


def memorize_goal(pole1, pole2):
    global r_last_pole1_seen
    global a_last_pole1_seen
    global r_last_pole2_seen
    global a_last_pole2_seen
    global turnto
    global poledoubt 
    if pole1 and pole2 == None:
        r_last_pole1_seen = pole1.position.r
        a_last_pole1_seen = pole1.position.a
        if (pole1.position.a > 0):
            turnto = 1
        else:
            turnto = -1
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
            # print("Poles memories are lost")
            r_last_pole1_seen = 0
            a_last_pole1_seen = 0
            r_last_pole2_seen = 0
            a_last_pole2_seen = 0
            poledoubt = 0


#socket_thread = threading.Thread(target=TauraGameController.socket_recieve) 
#socket_thread.start()

while robot.updateSimulation():
    world = robot.perceiveWorld()
    
    #id_robot = robot.index
    #team_name = robot.team
    
    #if(TauraGameController.data["time"] < 600):x
    if not world:
        sys.exit("No world received")
 
    robot.setKick(0)
    ball = search_ball()
    if ball:
        pole1, pole2 = search_goal()
        memorize_goal(pole1, pole2)
        flag = go_after_goal(pole1,pole2)

        if flag:
            stay_at_goal_center(pole1, pole2)
            block_ball_passing(pole1, pole2, ball)
	
        memorize_ball(ball)
       
    elif r_last_ball_seen  > balldoubt: 
        balldoubt = balldoubt + increases_balldoubt

    else:
        look_around()
  	
    time.sleep(1/10)
    #else:
      # stop_to_walk()
