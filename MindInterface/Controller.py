from MindInterface.config import *
from MindInterface.Model import *
from MindInterface.Communicator import *
import sys

graphic_mode = config["gui"]
if graphic_mode:
    from MindInterface.View import *
else:
    print("Mind interface not using graphic mode.")



class Controller:
    """This is the interface to control the robot."""

    def __init__(self, index):
        """
        Initializes the graphic interface if set, creates `world` object that 
        stores a list of objects detected on the world, stores the index of 
        which robot it should communicate to and initializes the JSON message.
        """
        self.graphic_mode = graphic_mode

        if self.graphic_mode:

            self.view = View()

        self.world = World()
        self.worldModel = WorldModel()
        self.index = index
        self.imu = 0
        # movement_vector = (radius, alpha, phi)
        # radius and alpha define where the robot wanna go
        # phi define the amount of angles the robot wants to rotate

        self.message = {'index': index}
        self.communicator = Communicator(self.index)

    def perceiveWorld(self):
        """Returns the world object, which contain the list of objects detected
        on the world."""
        return self.world

    def resetCommands(self):
        self.message = {'index': self.index}

    def updateSimulation(self):
        """Refreshes the screen if graphic mode is set and comunicates with the 
        robot sending commands and getting information about the world."""

        if self.graphic_mode:
            for event in pygame.event.get():
                if event.type == QUIT:
                    print("")
                    return False
                elif  event.type == KEYDOWN:
                    if event.key == K_q:
                        return False
        
        self.worldModel.update(self.world.objects_list)
        self.createWorldFromDict(self.communicator.communicate(self.message))
        self.resetCommands()

        if self.graphic_mode:
            self.view.update(self.world)

        return True

    def createWorldFromDict(self, wdict):
        """Receives a python dictionary and creates a list of objects"""
        if wdict:
            self.world.objects_list = []

            self.imu = wdict['imu']

            for obj in wdict['objects_list']:
                new_obj = BaseObject(
                    Point2(polarCoords=obj['position']), obj['kind']
                )
                self.world.objects_list.append(new_obj)
            # self.head_angle = wdict['head_angle']

    def getImu(self):
        return self.imu

    def setMovementVector(self, movement_vector: Point2):
        """Sets the movement vector that makes the robot move. The format is 
        Point2(r, a, phi)"""
        if movement_vector.r > 1:
            print("You can't walk faster than your maximum speed")
        else:
            self.message['movement_vector'] = movement_vector.getCoords(isRect=False, getPhi=True)

    def setNeck(self, neck: (float, float)):
        self.message['neck'] = neck

    def setKick(self, kick: int):
        """Sets the kick command being 0 no kick, 1 left leg kick and -1 right
        leg kick"""
        self.message['kick'] = kick

    def play(self, action: int):
        self.message['play'] = action
