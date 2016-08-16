from MindInterface.config import *
from math import *
import json

UNKNOWN, BALL, POLE, ROBOT = "unkown", "ball", "pole", "robot"
x, y = 0, 1
WALK = 0

class BaseObject(object):
    """This class defines what attributes a basic object should have. This is 
    the objects the robot can detect."""
    def __init__(self, pos, kind = UNKNOWN):
        """Initializes the object with a position and a kind.
        Position is a tuple of (r,a).
        Kind is one of the strings ["ball", "pole", "robot", "unkown"]."""
        self.position = pos
        self.kind = kind

    def getJSON(self):
        """Returns the JSON object of this object."""
        return json.dumps(self, default=lambda o: o.__dict__)

class World:
    """This class stores a list of objects detected by the robot. This list is 
    refreshed everytime the simulation is updated (everytime the robot receives 
    information about the world)"""
    def __init__(self):
        """Initializes the `objects_list` attribute as an empty list"""
        self.objects_list = []

    def getJSON(self):
        """Returns the JSON object of this object"""
        return json.dumps(self, default=lambda o: o.__dict__)
        #, sort_keys=True, indent=4)

    def getDict(self):
        """Returns the list as a python dictionary"""
        return json.loads(self.toJSON())

################################## 
#        World Modeling          #
##################################

class Thing:
    def __init__(self, kind: str, pos: Point2):
        self.kind = kind
        self.position = pos
        self.radius = 100
        self.hits = 1
        self.persistence = 1.0

class WorldModel(World):

    def __init__(self):
        self.things_list  = []
        self.objects_list = []

    def update(self, objects_list):
        for obj in objects_list:
            found_hit = False
            for thing in self.things_list:
                if thing.kind == obj.kind:
                    if abs((thing.position - obj.position).r) < thing.radius:
                        thing.position.x += obj.position.x
                        thing.position.y += obj.position.y
                        thing.hits += 1
                        thing.persistence += 1.0
                        found_hit = True
            if not found_hit:
                self.things_list.append(Thing(obj.kind, obj.position))
        self.objects_list.clear()
        for thing in self.things_list:
            thing.position.r /= thing.hits
            thing.hits = 1
            thing.persistence *= 0.99
            if thing.persistence < 0.5:
                self.things_list.remove(thing)
            elif thing.persistence > 2.0:
                self.objects_list.append(BaseObject(thing.position, thing.kind))