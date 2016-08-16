from MindInterface.config import *
from math import *
import socket
import json


class Communicator:
    """This class makes the communication via UDP sockets between the agent and 
    the robot it controls.
    """
    def __init__(self, index = 0):
        """Initializes the address for communication, if no ip address is given
        it defaults to localhost. Two socket objects are created, one for 
        talking and one for listening aswell as the ports for talking and 
        listening. Also, it sets the index of which robot it should communicate
        to.
        """
        self.address = config["address"]
        self.talk_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.index = index
        self.talking_port = INITIAL_PORT + (index * 2)
        self.listening_port = self.talking_port + 1

        self.listen_sock.bind((LOCALHOST, self.listening_port))

    def createMessage(self, msg):
        """Receives a python dictionary and returns its equivalent as a JSON 
        string"""
        message = msg
        return json.dumps(message)

    def talk(self, msg):
        """Tries to send the message from the agent to the body, being this
        body simulated or not."""
        message = self.createMessage(msg)
        if config["debug"]: print("Mind sent:", message)
        self.talk_sock.sendto(bytes(message, 'UTF-8'), (self.address, self.talking_port))

    def listen(self):
        """Tries to receive the message from the body, being this body simulated
        or not. It returns the world as a dictionary."""
        try:
            self.listen_sock.settimeout(1)
            data, addr = self.listen_sock.recvfrom(1024)
            message = data.decode('UTF-8')
            if config["debug"]: print("Mind received:", message)
            world_dict = json.loads(message)
            return world_dict
        except socket.error:
            if config["debug"]: print("Socket Error:", socket.error.errno)
            return {}

    def communicate(self, msg):
        """Talks and returns the message received as response."""
        self.talk(msg)
        return self.listen()
