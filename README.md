## Introduction

This is the simulation system for development of high level strategies 
created by the brazilian RoboCup team Taura Bots. It works as a server/client
system where the server is where the perception and action is done and the 
client is where the mind of the agent is programmed, receiving data about the 
objects perceived in the world and sending commands to be persisted in the world
 by the body.

## Installation
You will need *python 3.x*. On ubuntu simply use the command:

```
sudo apt-get install python3
```
The application uses the graphic library *pygame*. The problem is pygame doesn't
 work on *python 3* so you will have to download the source code of *pygame* and
 compile it with *python 3*

You can do it following the steps:

1. Go to your home directory
```
cd ~
```
2. Download *mercurial* to get the *pygame* source code
```
sudo apt-get install mercurial
```
3. Clone the source code and go inside it's directory
```
hg clone https://bitbucket.org/pygame/pygame
cd pygame
```
4. Install the dependencies to compile *pygame*
```
sudo apt-get install python3-dev python3-numpy libsdl-dev libsdl-image1.2-dev \
libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev \
libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev
```
(the three lines above are all one single command)
5. Build the project using *python 3*
```
python3 setup.py build
```
6. Install *pygame* using *python 3*
```
sudo python3 setup.py install
```
7. Test it
```
python3
>>> import pygame
```
If no error is raised, your installation of *pygame* with *python 3* worked! :)

## Usage
To simulate the world: 
```
python3 WorldSimulation.py
```
You can use `python3 WorldSimulation.py -h` will give you help on how to use 
parameters.

To create an artificial intelligence to control a robot, use the AI.py file as 
reference.

--------------------------------------------------------------------------------
## The Controller class

An instance of the Controller class is returned when you start a simulation.

```
# Simulation methods
updateSimulation()
perceiveWorld()

# Robot controlling methods
setMovementVector(movement_vector: Point2)
setKick(kick: int)
```

Using a method to control the robot will write the attribute with the value 
passed. This means that if you set the robot to walk forward it will do it until
 you tell it to stop.

### `updateSimulation() -> Bool`

Refreshes the graphic interface (if used) and communicates with the "body" of 
the robot to perceive the environment.

Returns `True` while everything is running fine.

### `perceiveWorld() -> World`

Returns an instance of the `World` class containing information about the 
environment. The `World` class only have one attribute which is `objects_list`.

### `setMovementVector(movement_vector: Point2)`

Receives a movement vector in the format (speed, angle, phi) where:

- `speed` is a number between 0 and 1 setting from 0% to 100% of the robot speed
Example: 
```
speed = 0.5 # will set the speed to 50% of max robot speed
```

- `angle` is the direction to where the robot should move ranging from -pi to pi
Example: 
```
angle = 0     # straight forward
angle = pi/2  # 90° to the left
angle = -pi/4 # 45° to the right
```

- `phi` is an angle between pi and -pi setting the rotation of the robot.
Example:
```
phi = 0  # robot keep facing forward
phi = pi # robot will rotate left trying to face backwards
```
Keep in mind that the rotation has a limitation of pi/18 so the robot will 
rotate pi/18 even when set to rotate more than that.

The Point2 should be created like this: 
`movement_vector = Point2(r=speed, a=angle, phi=phi)`

### `setKick(kick: int)`

Receives a number representing the kick where 0: no kick, 1: left leg kick, -1:
 right leg kick
