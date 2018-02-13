import pygame

class Arena():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.text = self.font.render("direction", True, (0, 128, 0))
        self.pos = self.font.render("pos!", True, (0, 128, 0))


        pygame.display.set_caption('trekker_sim')

        self.DISPLAY = pygame.display.set_mode((640, 480), 0, 32)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.green = (0, 255, 0)

    def setPos(self, pos):
        self.pos = self.font.render("object_pos:"+pos, True, (255, 255, 255))

    def setText(self, action):

        direction = ''

        if action == 0:  # up
            direction = 'up'
        if action == 1:  # down
            direction = 'down'

        if action == 2:  # left
            direction = 'left'
        if action == 3:  # right
            direction = 'right'
        if action == 4:  # stop
            direction = 'stop'

        self.text = self.font.render("robot_move:"+direction, True, (255, 255, 255))

    def drawArena(self):
        self.DISPLAY.fill(self.BLACK)
        self.DISPLAY.blit(self.text, (10,10))
        self.DISPLAY.blit(self.pos, (10,30))


        pygame.draw.line(self.DISPLAY, (0, 0, 255), (0, 240), (640, 240))
        pygame.draw.line(self.DISPLAY, (0, 0, 255), (320, 0), (320, 480))
        pygame.draw.circle(self.DISPLAY, self.BLUE, (320, 240), 5, 0)

    def drawRobot(self, position):
        self.drawArena()


        pygame.draw.circle(self.DISPLAY, self.RED, (int(float(position.item(0))), int(float(position.item(1)))), 5, 0)
        pygame.draw.circle(self.DISPLAY, self.YELLOW, (int(float(position.item(0))), int(float(position.item(1)))), 30, 1)
        pygame.display.update()