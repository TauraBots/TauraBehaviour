from World.config import *
from World.Controller import *

def start():
    pygame.init()
    world_controller = Controller()

    clock = pygame.time.Clock()
    play = True
    while play:
        clock.tick(60)
        play = world_controller.updateSimulation()


if __name__ == "__main__":
    start()