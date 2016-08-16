import random
from libs.Point2 import *
from math import *


def generateUncertainty(radius):
    u_radius = random.random() * radius
    u_angle = random.random() * 2*pi

    return Point2(r=u_radius, a=u_angle)

def toPolar(point):
    x = point[0]
    y = point[1]
    return (sqrt(x**2 + y**2), atan2(y, x))

def toRectangular(point):
    r = point[0]
    a = point[1]
    return (r * cos(a), r * sin(a))

def normalizeAngle(angle):
    while angle > pi:
        angle = angle - 2*pi
    while angle < -pi:
        angle = angle + 2*pi
    return angle

def limitAngle(angle, limit):
    # print("angle", degrees(angle),"transformed to", end=" ")
    if angle > limit:
        angle = limit
    elif angle < -limit:
        angle = -limit
    # print(degrees(angle))
    return angle
