from World.config import *
from World.Model import *
from pygame import Color
from pygame import draw
from pygame.time import Clock

class W_GraphicObject:
    def __init__(self, obj):
        self.position = obj.position.getCoords()
        self.uncertainty = obj.uncertainty
        self.kind = obj.kind

        self.size = 5
        self.color = Color('white')
        self.neck_pan = 0.0
        self.body_angle = 0.0
        self.movement_vector = (0, 0)
        self.kick_vector = (0, 0)

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
            self.head_abs_angle = obj.neck_pan + obj.body_angle
            self.body_angle = obj.body_angle
            self.movement_vector = obj.movement_vector
            self.vision_width = obj.vision_width

class WorldView:
    def __init__(self):
        self.screen = {
            'width': WIDTH,
            'height': HEIGHT,
            'surface': None,
            'background': Color(0, 122, 0)
        }
        self.help = True
        pygame.display.set_caption('TauraSim - World Simulation')
        self.screen['surface'] = pygame.display.set_mode(
            (self.screen['width'], self.screen['height']), 0, 32)
        self.mouse_position = (0, 0)
        self.clock = Clock()

    def setMousePosition(self, pos):
        self.mouse_position = pos

    def update(self, world):
        self.drawField()
        self.drawWorld(world)
        if self.help:
            self.drawHelp()
        pygame.display.flip()
        self.clock.tick(FPS)
        # print(self.clock.get_fps(), end="\r")

    def blitSurface(self, surface, position):
        self.screen['surface'].blit(surface, position)

    def drawHelp(self):
        font = pygame.font.SysFont("monospace", 15)
        help_string = [
            "r - insert robot",
            "b - insert ball",
            "p - insert pole",
            "o - insert unknown object",
            "h - show/hide this help message",
            "q - quit",
            "left/right - rotates the robot's body",
            "a/d - rotates the robot's head",
            "scroll - increase/decrease object's uncertainty"]

        for i, string in enumerate(help_string):
            surf = font.render(string, True, (0,0,0))
            self.blitSurface(surf, (30, 15 + i*15))

        font = pygame.font.SysFont("monospace", 10)

        h = self.screen['height']
        for i in range(0, h, 25):
            surf = font.render(str(i), True, (0,0,0))
            self.blitSurface(surf, (0, i - 10))

        for i in range(0, self.screen['width'], 25):
            surf = font.render(str(i), True, (0,0,0))
            self.blitSurface(surf, (i, h - 10))



    def drawField(self):
        self.screen['surface'].fill(self.screen['background'])

        h_poly_pts = [
            (0, self.mouse_position[1] + 2),
            (0, self.mouse_position[1] - 2),
            (5, self.mouse_position[1])
        ]
        draw.polygon(self.screen['surface'], (0,0,0), h_poly_pts)

        w_poly_pts = [
            (self.mouse_position[0] + 2, self.screen['height']),
            (self.mouse_position[0] - 2, self.screen['height']),
            (self.mouse_position[0], self.screen['height'] - 5)
        ]
        draw.polygon(self.screen['surface'], (0,0,0), w_poly_pts)

    def drawWorld(self, world):
        for obj in world.objects_list:
            self.drawObject(W_GraphicObject(obj))

    def drawObject(self, obj):
        obj_area = obj.size*2
        unc_area = (obj.uncertainty * 2) + obj_area

        unc_surface = pygame.Surface((unc_area, unc_area))
        unc_surface.fill(self.screen['background'])
        unc_surface.set_colorkey(self.screen['background'])
        unc_surface.set_alpha(122)
        unc_surface_center = (int(unc_area/2), int(unc_area/2))
        pygame.draw.circle(unc_surface, obj.color, unc_surface_center, int(unc_area/2))

        obj_surface = pygame.Surface((obj_area, obj_area))
        obj_surface.fill(self.screen['background'])
        obj_surface.set_colorkey(self.screen['background'])
        obj_surface_center = (obj.size, obj.size)
        rect = pygame.draw.circle(obj_surface, obj.color, obj_surface_center, obj.size)


        if obj.kind == ROBOT:
            # desenhar orientação da cabeça
            end_pos = toRectangular( (obj.size, - obj.head_abs_angle) )
            end_pos = (
                obj_surface_center[0] + end_pos[0],
                obj_surface_center[1] + end_pos[1]
            )
            pygame.draw.line(obj_surface, (255,0,0), obj_surface_center, end_pos, 3)
            # desenhar parte preta que representa as costas do robô
            pygame.draw.arc(obj_surface, (0,0,0), rect, obj.body_angle + pi/2, obj.body_angle + 3*pi/2, obj.size)

            # desenha o vetor de movimento
            movement_size = 25
            obj.movement_vector = obj.movement_vector.getCoords()
            movement_point =(
                obj_surface_center[0] + obj.movement_vector[0] / 1 * movement_size,
                obj_surface_center[1] + obj.movement_vector[1] / 1 * movement_size
            )
            pygame.draw.line(obj_surface, (255,0,255), obj_surface_center, movement_point, 3)

            # campo de visão
            vision_width = obj.vision_width
            vision_range = 100

            vision_surface = pygame.Surface((vision_range * 2, vision_range * 2))
            vision_surface.fill(self.screen['background'])
            vision_surface.set_colorkey(self.screen['background'])
            vision_surface.set_alpha(200)
            vision_surface_center = (vision_range, vision_range)

            angle_1 = - obj.head_abs_angle + vision_width/2
            angle_2 = - obj.head_abs_angle - vision_width/2

            point_1 = (vision_range, angle_1)
            point_2 = (vision_range, angle_2)

            point_1 = toRectangular(point_1)
            point_2 = toRectangular(point_2)

            point_1 = (point_1[0] + vision_surface_center[0], point_1[1] + vision_surface_center[1])
            point_2 = (point_2[0] + vision_surface_center[0], point_2[1] + vision_surface_center[1])

            pygame.draw.line(vision_surface, (120,120,120), vision_surface_center, point_1, 5)
            pygame.draw.line(vision_surface, (120,120,120), vision_surface_center, point_2, 5)

            position = (
                obj.position[0] - vision_range,
                obj.position[1] - vision_range
            )
            self.blitSurface(vision_surface, position)







        position = (
            obj.position[0]-unc_area/2,
            obj.position[1]-unc_area/2
        )
        self.blitSurface(unc_surface, position)

        position = (
            obj.position[0]-obj.size,
            obj.position[1]-obj.size
        )
        self.blitSurface(obj_surface, position)
