import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
font = pg.font.SysFont("arialblack", 20)
objects = []


class Button:
    def __init__(self, x, y, width, height, buttonText='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (52, 78, 91))

        objects.append(self)

    def process(self):
        action = False
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0] == 1 and self.alreadyPressed is False:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.alreadyPressed = True
                action = True
            if pg.mouse.get_pressed(num_buttons=3)[0] == 0:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
        return action
