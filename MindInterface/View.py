from MindInterface.config import *
from MindInterface.Model import *
import pygame
from pygame.locals import *
from pygame import Color
from pygame import draw
from math import *

class GraphicObject:
    def __init__(self, obj):
        self.position = obj.position
        self.kind = obj.kind
        if obj.kind == UNKNOWN:
            self.size = OBJ_RADIUS
            self.color = Color('#000000')
        elif obj.kind == BALL:
            self.size = OBJ_RADIUS
            self.color = Color('#FFFFFF')
        elif obj.kind == POLE:
            self.size = OBJ_RADIUS
            self.color = Color('#EE9900')
        elif obj.kind == ROBOT:
            self.size = ROBOT_RADIUS
            self.color = Color('#0099EE')

class View:
    def __init__(self):
        self.screen = {
            'width': 500,
            'height': 500,
            'surface': None,
            'center': (int(500/2), int(500/2))
        }
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('TauraSim - Mind Interface')
        self.screen['surface'] = pygame.display.set_mode(
            (self.screen['height'], self.screen['width']), 0, 32)

    def getCenter(self):
        return self.screen['center']

    def update(self, world):
        self.drawField()
        self.drawWorld(world)

        pygame.display.flip()
        self.clock.tick(60)

    def drawField(self):
        self.screen['surface'].fill((0,0,122))

    def drawWorld(self, world):
        # desenha uma circunferência representando o próprio robô
        pygame.draw.circle(self.screen['surface'], Color('#0099EE'), (self.getCenter()[0], self.screen['height']), 5)
        for obj in world.objects_list:
            self.drawObject(GraphicObject(obj))

    def drawObject(self, obj):
        # gira 90° para ficar com o 0 para frente
        # -90° pq com o y crescendo pra baixo o angulo aumenta anti-horário

        angle = obj.position.a
        angle *= -1
        angle -= pi/2
        # converte para retangulares para exibir na tela
        pos = Point2(r=obj.position.r, a=angle)
        # translada da origem para o centro da tela
        pos = (self.getCenter()[0] + int(pos.x), self.screen['height'] + int(pos.y))

        pygame.draw.circle(self.screen['surface'], obj.color, pos, obj.size)