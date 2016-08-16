########################################
#   IA TauraBots Version 1.0.0 beta    #
#   Author: Fábiner de Melo Fugali     #
#   Date: 15/10/2015                   #
########################################


from MindInterface import Simulation 
from MindInterface.config import *   

import time
import math

# Starts the simulation and stores a reference to the robot you are controlling
robot = Simulation.start()

# Last ball seem informations
a_last_ball_seem = 0.0
p_last_ball_seem = pi/2
r_last_ball_seem = 0

# Doubt about ball
balldoubt = 0

# Identifier 1 or -1 to starts by default to turn around ball anticlockwise
turnto = 1

# Memory for poles
a_last_pole1_seem = 0
r_last_pole1_seem = 0
a_last_pole2_seem = 0
r_last_pole2_seem = 0

# Variable that defines if Memory of poles will be lost or not
poledoubt = 0

# Last object position is blocking me
a_last_obstacle_position = 0


def look_around():
    robot.setMovementVector( Point2(r=0, a=a_last_ball_seem,phi=p_last_ball_seem) )


def search_ball():
    for obj in world.objects_list:
        # If some object has kind ball
        if obj.kind == "ball":
            # That object is the ball!
            return obj    
    return None


def search_goal():
    found = 0
    pole1 = None
    pole2 = None
    global r_last_pole2_seem
    global a_last_pole2_seem
    for obj in world.objects_list:
        # If some object has kind pole
        if obj.kind == "pole":
            found = found + 1
            # That object is the pole!
            if found == 1:
                pole1 = obj
                # If the object will be between 0.5 and -0.5 of last past position. It is the same pole1, else will be pole2
                if pole1.position.a < a_last_pole1_seem - pi/6 or pole1.position.a > a_last_pole1_seem + pi/6:
                    r_last_pole2_seem = r_last_pole1_seem
                    a_last_pole2_seem = a_last_pole1_seem
            if found == 2:
                pole2 = obj
    return pole1, pole2


def obstacle_detection(b):
    # Avoid obtacles
    for obj in world.objects_list:
        # If some object is obstacle
        if obj.position.a > b.position.a -pi/2 and obj.position.a < b.position.a + pi/2 and b.position.r > 30 and obj.kind != "ball" and obj.position.r < b.position.r and obj.position.r < 30:
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
      

def avoid_by_left():
    robot.setMovementVector(Point2(r=1,a= pi/2,phi= pi/2)) 


def avoid_by_right():
    robot.setMovementVector(Point2(r=1,a= -pi/2,phi= pi/2))


def go_after_ball(ball):
    global a_last_obstacle_position
# If ball is far or lost align to ball
    if ball.position.r > 30 or (ball.position.a < -0.1 or ball.position.a > 0.1):
        # Variable for notify if there is obtacle
        obstacle = obstacle_detection(ball) 
        if obstacle:
            obstacle_avoidance(obstacle)
            a_last_obstacle_position = obstacle.position.a 
        else:
            walk_to_something(ball.position.a, ball.position.a)
     
        # Verify if I can move myself to direction of ball
        if r_last_ball_seem > ball.position.r - 0.1 and r_last_ball_seem < ball.position.r + 0.1 and ball.position.r > 30:
            print("I can't move!")
            if a_last_obstacle_position < 0:
                walk_side_left()
            if a_last_obstacle_position > 0:
                walk_side_right()    
        return 0
    else:
        return 1


def walk_to_something(alpha, phi):
    robot.setMovementVector( Point2(r=1, a=alpha, phi=phi) )

  
def walk_side_left():
    robot.setMovementVector(Point2(r=1,a= pi/2,phi= 0))


def walk_side_right():
    robot.setMovementVector(Point2(r=1,a= -pi/2,phi= 0)) 


def stop_to_walk():
    robot.setMovementVector( Point2() )


def opposite_to_goal_center(p1, p2):
    if p1 and p2:
        print("p1 and p2")
        if(((p1.position.a + p2.position.a)/2) < 0):
            # Turn around ball anticlockwise
            turn_around_ball( 1)
        else:
            # Turn around ball clockwise
            turn_around_ball(-1)
    elif p1:
        print("p1")
        if (p1.position.a + a_last_pole2_seem)/2 < 0:
            # Turn around ball anticlockwise
            turn_around_ball( 1)
        else:
            # Turn around ball clockwise
            turn_around_ball(-1)


def turn_around_ball(t):
    robot.setMovementVector( Point2(r=1, a=pi/2*t,phi=-pi/2*t) )


def kick(p1, p2, b):
    # If I have pole1 and pole2 then kick at center of poles
    if p1 and p2 and b:
        if((p1.position.a + p2.position.a)/2 > -0.1 and (p1.position.a + p2.position.a)/2 < 0.1):
            print("kick")
            if b.position.a > 0:
                left_kick()
            else:
                right_kick()
    # If only found one pole, kick in this direction
    elif p1 and b: 
        # If is too far away, then align to the only pole1 seem with the last position of pole2 and kick to.
        if ((p1.position.a + a_last_pole2_seem)/2 > -0.1 and (p1.position.a + a_last_pole2_seem)/2 < 0.1):
            print("kick")
            if b.position.a > 0:
                left_kick()
            else:
                right_kick()
    # Search pole   
    elif p1 == None:
        # Turn around ball 
        print("é aqui q eu to movendo miltinho")
        robot.setMovementVector( Point2(r=1, a=-pi/2 * turnto, phi=pi/2 * turnto) )


def left_kick():
    robot.setKick( 1)


def right_kick():
    robot.setKick(-1)


def memorize_ball(b):
    global a_last_ball_seem
    global p_last_ball_seem
    global r_last_ball_seem
    global balldoubt
    a_last_ball_seem = b.position.a
    p_last_ball_seem = b.position.a
    r_last_ball_seem = b.position.r
    balldoubt = 0

def memorize_goal(pole1, pole2):
    global r_last_pole1_seem
    global a_last_pole1_seem
    global r_last_pole2_seem
    global a_last_pole2_seem
    global turnto
    global poledoubt 
    if pole1 and pole2 == None:
        r_last_pole1_seem = pole1.position.r
        a_last_pole1_seem = pole1.position.a
        if (pole1.position.a > 0):
            turnto = 1
        else:
            turnto = -1
        poledoubt = 0
    if pole1 and pole2:
        r_last_pole1_seem = pole1.position.r
        a_last_pole1_seem = pole1.position.a
        r_last_pole2_seem = pole2.position.r
        a_last_pole2_seem = pole2.position.a        
        poledoubt = 0
    if pole1 == None and pole2 == None:
        poledoubt = poledoubt + 1
        if poledoubt > 40:
            # Lost the memory of last poles position
            print("Poles memories are lost")
            r_last_pole1_seem = 0
            a_last_pole1_seem = 0
            r_last_pole2_seem = 0
            a_last_pole2_seem = 0
            poledoubt = 0


while robot.updateSimulation():
    world = robot.perceiveWorld()
    if not world:
        sys.exit("No world received")
 
    robot.setKick(0)
    ball = search_ball()
    if ball:
        pole1, pole2 = search_goal()
        memorize_goal(pole1, pole2)
        flag = go_after_ball(ball)

        if flag:
            stop_to_walk()
            opposite_to_goal_center(pole1, pole2)
            kick(pole1, pole2, ball)
			
        memorize_ball(ball)
       
    elif r_last_ball_seem  > balldoubt: 
        walk_to_something(a_last_ball_seem, a_last_ball_seem)
        balldoubt = balldoubt + 10

    else:
        look_around()
  	
    time.sleep(1/10)

# To do List
# Implement ball track prevision


# Done List
# After some time, set the poles memory to zero
# Ball doubt
# Pole doubt
# Prevision of Obstacles
# Avoid obstacles
# Kick only to goal
# Change poles memory
