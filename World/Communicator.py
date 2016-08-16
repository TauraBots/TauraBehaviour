from World.config import *

import socket
import json
from World.Model import *
import random

class Communicator:
    def __init__(self, index, world):
        self.address = config["address"]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.index = index
        self.listening_port = INITIAL_PORT + (index * 2)
        self.talking_port = self.listening_port + 1
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.address, self.listening_port))

        self.world = world

    def isThisObjMyRobot(self, obj):
        if obj.kind != ROBOT:
            return False
        elif obj.index == self.index:
            return True
        else:
            return False

    def createMessage(self):
        world = {
            'objects_list': []
        }
        my_robot = self.world.getRobots()[self.index]
        obj_list = self.world.getEgocentric(my_robot)

        for obj in obj_list:
            obj.position.a += my_robot.neck_pan
            obj_dict = {
                'position': obj.position.getCoords(False, getPhi=True),
                'kind': obj.kind
            }
            world['objects_list'].append(obj_dict)

        world['imu'] = my_robot.body_angle
        # world['head_angle'] = my_robot.head_angle
        return json.dumps(world)


    def talk(self):
        message = self.createMessage()
        if config["debug"]: print("Body sent:", message)
        self.sock.sendto(bytes(message, 'UTF-8'), (self.address, self.talking_port))

    def listen(self):
        # print('Server listening...')
        try:
            self.sock.settimeout(1/100)
            data, addr = self.sock.recvfrom(1024)
            message = data.decode('UTF-8')
            if config["debug"]: print("Body received:", message)
            return json.loads(message)
        except socket.error:
            # print(socket.error.errno)
            pass
        return False