from World.config import *
from World.Model import *
from World.View import *
from World.Communicator import *

class Controller:
    def __init__(self):
        self.world = W_WorldModel()
        self.view = WorldView()
        self.communicators = []

        self.mouse_position = Point2(0, 0)
        self.moving_obj = None
        self.rel_click_pos = Point2(0, 0)

    def removeObject(self):
        clicked_obj = self.world.checkCollision(self.mouse_position)
        if clicked_obj in self.world.objects_list:
            index = self.world.objects_list.index(clicked_obj)
            del self.world.objects_list[index]

    def setMovingObject(self):
        clicked_obj = self.world.checkCollision(self.mouse_position)
        if clicked_obj:
            self.moving_obj = clicked_obj
            obj_pos = clicked_obj.position
            click_pos = self.mouse_position
            self.rel_click_pos = click_pos - obj_pos
        else:
            self.moving_obj = None


    def updateSimulation(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            else:
                if not self.handleEvent(event):
                    return False

        for robot in self.world.getRobots():
            if robot.kick != 0:
                self.world.robotKick(robot)

        self.world.moveObjects()
        self.communicate()

        self.view.update(self.world)
        return True

    def communicate(self):
        for communicator in self.communicators:
            message = communicator.listen()
            if message:
                robot = self.world.robots_list[message['index']]

                if 'movement_vector' in message.keys():
                    mv_vector = Point2(
                        r   = message['movement_vector'][0], 
                        a   = message['movement_vector'][1], 
                        phi = message['movement_vector'][2]
                    )

                    # corrigir o angulo do movimento de acordo com o angulo do corpo
                    mv_vector.a = mv_vector.a + robot.body_angle
                    
                    # inverte o Y
                    mv_vector.a = mv_vector.a * -1
                    mv_vector.r = mv_vector.r * ROBOT_MAX_SPEED
                    robot.setMovementVector(mv_vector)

                if 'kick' in message.keys():
                    robot.setKick(message['kick'])
                    
                if 'neck' in message.keys():
                    robot.setNeckPan(message['neck'][0])
                else:
                    robot.setNeckPan(0)

                communicator.talk()

    def checkMovingObject(self):
        if self.moving_obj:
            button_pressed,_,_ = pygame.mouse.get_pressed()
            if button_pressed:
                new_position = self.mouse_position - self.rel_click_pos
                radius = OBJ_RADIUS
                if self.moving_obj.kind == ROBOT:
                    radius = ROBOT_RADIUS
                if not self.world.checkCollision(new_position, radius, self.moving_obj):
                    self.moving_obj.position = new_position
            else:
                self.moving_obj = None


    def handleEvent(self, event):
        if event.type == MOUSEMOTION:
            self.mouse_position = Point2(rectCoords=pygame.mouse.get_pos())
            self.view.setMousePosition(self.mouse_position.getCoords())
            self.checkMovingObject()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1: self.setMovingObject() # left click
            elif event.button == 3: self.removeObject() # right click
            elif event.button == 5: # scroll UP
                obj = self.getClosestObject()
                obj.uncertainty += 1
            elif event.button == 4: # scroll DOWN
                obj = self.getClosestObject()
                if obj.uncertainty -1 >= 0:
                    obj.uncertainty -= 1
        elif event.type == KEYDOWN:
            # create object
            if event.key in objectKeys.keys():
                self.createObject(event.key)
            # control closest robot
            elif event.key in controlKeys:
                self.controlRobot(self.getClosestRobot(), event.key)
            # show / hide help
            elif event.key == K_h:
                self.view.help = not self.view.help
            # quit
            elif event.key == K_q:
                return False
        elif event.type==VIDEORESIZE:
            screen=pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE, 32)
        return True


    def createObject(self, key):
        new_object = None
        mouse_vector = self.mouse_position
        if key == K_r:
            if not self.world.checkCollision(mouse_vector, ROBOT_RADIUS):
                new_object = W_RobotModel(mouse_vector, ROBOT, self.world)
                robot_index = len(self.world.getRobots())
                new_object.index = robot_index
                self.communicators.append(Communicator(robot_index, self.world))
                self.world.robots_list.append(new_object)
        elif not self.world.checkCollision(mouse_vector, OBJ_RADIUS):
            new_object = W_BaseObjectModel(mouse_vector, objectKeys[key])
        if new_object:
            self.world.objects_list.append(new_object)

    def getClosestObject(self):
        lowest_distance = 999999999.9
        closest_object = None
        for obj in self.world.objects_list:
            distance = (obj.position - self.mouse_position).r
            if distance < lowest_distance:
                closest_object = obj
                lowest_distance = distance
        return closest_object

    def getClosestRobot(self):
        lowest_distance = 999999999.9
        closest_robot = None
        for obj in self.world.objects_list:
            if obj.kind == ROBOT:
                distance = (obj.position - self.mouse_position).r
                if distance < lowest_distance:
                    closest_robot = obj
                    lowest_distance = distance
        return closest_robot

    def controlRobot(self, robot, key):
        if robot:
            if key == K_RIGHT:
                robot.body_angle -= robot.body_angle_step
            elif key == K_LEFT:
                robot.body_angle += robot.body_angle_step
                pass
            elif key == K_d:
                if (robot.neck_pan - robot.neck_pan_step) >= -(pi/2):
                    robot.neck_pan -= robot.neck_pan_step
            elif key == K_a:
                if (robot.neck_pan + robot.neck_pan_step) <= (pi/2):
                    robot.neck_pan += robot.neck_pan_step
