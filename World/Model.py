from World.config import *
import copy


class W_BaseObjectModel(object):
    def __init__(self, pos = Point2(0, 0), kind = UNKNOWN):
        self.position = pos
        self.kind = kind
        self.uncertainty = 0
        self.velocity = Point2()

    def __repr__(self):
        return ("{1}:{{'position': ({0}), 'uncertainty': {2}}}".format(self.position, self.kind, self.uncertainty))

class W_RobotModel(W_BaseObjectModel):
    def __init__(self, pos, kind, world):
        super().__init__(pos, kind)
        self.neck_pan = 0.0
        self.neck_tilt = 0.0
        self.body_angle = 0.0
        self.neck_pan_step = pi/18
        self.neck_tilt_step = pi/18
        self.body_angle_step = pi/18
        self.neck_pan_limit = pi/2
        self.neck_tilt_limit = pi/2
        self.index = 0
        self.movement_vector = Point2(0.0, 0.0, 0.0)
        self.vision_width = pi/2
        self.world = world
        self.kick = 0
        self.imu = 0

    def setMovementVector(self, movement_vector):
        self.movement_vector = movement_vector
        self.move()

    def setNeckPan(self, angle):
        # limita o angulo para q seja um angulo válido
        angle = limitAngle(angle, self.neck_pan_limit)
        # calcula o incremento necessário para chegar ao angulo desejado
        increment = angle - self.neck_pan
        # limita o incremento para q seja no máximo do tamanho do passo
        increment = limitAngle(increment, self.neck_pan_step)

        self.neck_pan += increment

    def move(self):
        phi = self.movement_vector.phi

        self.body_angle += limitAngle(phi, self.body_angle_step)
        self.imu += limitAngle(phi, self.body_angle_step)


        new_position = self.position + self.movement_vector
        if not self.world.checkCollision(new_position, ROBOT_RADIUS, self):
            self.position = new_position
        # self.movement_vector = (0,0,0)

    def setKick(self, kick):
        self.kick = kick

class W_WorldModel:
    def __init__(self):
        self.objects_list = []
        self.robots_list = []

    def getRobots(self):
        robots = []
        for obj in self.objects_list:
            if obj.kind == ROBOT:
                robots.append(obj)
        return robots

    def getKickableBalls(self, robot):
        # W_RobotModel robot, int kick (-1 | 1)
        pos = Point2(vector=robot.position)
        balls = [o for o in self.objects_list if o.kind == "ball"]
        kickable_balls = []
        for ball in balls:
            b = Point2(vector=ball.position)
            b -= pos
            b.a += robot.body_angle
            b.r -= ROBOT_RADIUS
            if robot.kick == -1:
                if b.x > 0 and b.x < 13 and b.y < 8 and b.y > 0:
                    kickable_balls.append(ball)
            elif robot.kick == 1:
                if b.x > 0 and b.x < 13 and b.y < 0 and b.y > -8:
                    kickable_balls.append(ball)
        return kickable_balls


    def robotKick(self, robot):
        # passa pelos objetos do mundo
        
        for ball in self.getKickableBalls(robot):
                ball.velocity.r = 10
                # - angle because of reasons
                ball.velocity.a = -robot.body_angle

    def moveObjects(self):
        for obj in self.objects_list:
            if obj.velocity.r > 0.1:
                new_position = obj.position + obj.velocity
                obj2 = self.checkCollision(new_position, OBJ_RADIUS, obj)
                if not obj2:
                    obj.position = new_position
                    obj.velocity.r = obj.velocity.r * FRICTION
                    # print("not hitting anythin, should move")
                else:
                    collision = (obj2.position - obj.position)
                    distance = collision.r

                    angle = collision.a

                    obj.velocity.a -= angle
                    obj2.velocity.a -= angle

                    v1 = Point2(obj.velocity.x, obj.velocity.y)
                    v2 = Point2(obj2.velocity.x, obj2.velocity.y)

                    v1.x, v2.x = v2.x, v1.x

                    v1.a += angle
                    v2.a += angle

                    obj.velocity = Point2(v1.x, v1.y)
                    if obj2.kind == "ball":
                        obj2.velocity = Point2(v2.x, v2.y)

                    inside = (OBJ_RADIUS + OBJ_RADIUS) - distance

                    obj.position += Point2(r=inside/2, a=-collision.a)
                    if obj.kind == "ball":
                        obj2.position += Point2(r=inside/2, a=collision.a)

    def checkCollision(self, pos, r=0, check_obj=None):
        for obj in self.objects_list:
            if obj == check_obj:
                pass
            else:
                dist = (pos - obj.position).r
                radius = ROBOT_RADIUS if obj.kind == ROBOT else OBJ_RADIUS
                if dist < radius + r:
                    return obj
        return None

    def getEgocentric(self, robot):
        obj_list = self.objects_list
        final_list = []
        for obj in obj_list:
            # print("checando objeto")
            if obj != robot:
                # print("não é meu robô")
                # gera ruído de maneira polar
                unc_pos = generateUncertainty(obj.uncertainty)

                # soma à posição do objeto ao ruído
                obj_pos = obj.position + unc_pos

                # passa a posição com o ruído para um sistema onde o robô é a origem
                # essa é a posição relativa
                rel_pos = obj_pos - robot.position

                # converte a posição relativa para polar
                #polar_pos = toPolar(rel_pos)

                #angle = polar_pos[1]
                # soma o ângulo da cabeça + angulo do corpo
                robot_angle = robot.neck_pan + robot.body_angle
                angle = rel_pos.a + robot_angle

                # inverte o ângulo porque com o Y aumentando pra baixo o angulo aumenta em sentido anti-horário
                angle = angle * -1

                # normaliza o angulo
                # 0 ~ 2PI => PI ~ -PI
                angle = normalizeAngle(angle)

                limit_left = -robot.vision_width/2
                limit_right = robot.vision_width/2

                if angle > limit_left and angle < limit_right:
                    rel_pos.a = angle
                    rel_pos.r -= ROBOT_RADIUS
                    new_obj = copy.deepcopy(obj)
                    new_obj.position = rel_pos

                    final_list.append(new_obj)

        return final_list
