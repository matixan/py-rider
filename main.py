#This is a simple game where you are late to your Politechnika Poznańska exams.

# this is game engine importing
import pygame, sys, random
from pygame.locals import *
pygame.init()

import graphics # app specific module

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# limit FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# create window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
MENU_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
menu_window = pygame.display.set_mode(MENU_SIZE)
menu_window.fill(WHITE)
pygame.display.set_caption("PyRider - Politechnika Poznańska Edition")
icon = pygame.image.load('data/PP_logo_RGB.png')
pygame.display.set_icon(icon)

# create car
car = graphics.Car(175, 200, RED)

# create road
road = graphics.Road(0, 0, GREEN)

while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()      
            sys.exit()
     
    menu_window.fill(WHITE)
    car.draw(menu_window)
    road.draw(menu_window)

    pygame.display.update()
    FramePerSec.tick(FPS)