#This is a simple game where you are late to your Politechnika Poznańska classes.
#You have to drive as fast as you can to get there on time before the professor.
#You can change gears with UP and DOWN arrows.
#You are racing against professor on a straight 1/4 mile road.
#You can see your speed, RPM, gear and distance to the destination on the dashboard.
#You can pause the game by pressing P.
#if you loose, you are late to the classes and you have to try again next time.

#force download of pygame
try:
    import pygame
except ImportError:
    import os
    os.system("pip install pygame")
    import pygame

# this is game engine importing
import sys, random, time
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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MENU_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
menu_window = pygame.display.set_mode(MENU_SIZE)
menu_window.fill(WHITE)
pygame.display.set_caption("PyRider - Politechnika Poznańska Edition")
icon = pygame.image.load('data/PP_logo_RGB.png')
pygame.display.set_icon(icon)

# create welcome screen
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('Welcome to PyRider - Politechnika Poznańska Edition', True, (0, 0, 0))
text_rect = textsurface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
menu_window.blit(textsurface, text_rect)

textsurface = myfont.render('Press any key to start', True, (0, 0, 0))
text_rect = textsurface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
menu_window.blit(textsurface, text_rect)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            break
        if event.type == QUIT:
            pygame.quit()      
            sys.exit()
    if event.type == pygame.KEYDOWN:
        break
    FramePerSec.tick(FPS)

# create road
road = graphics.Road(SCREEN_WIDTH, SCREEN_HEIGHT)

# create cars
car = graphics.Car(SCREEN_WIDTH/2+25, SCREEN_HEIGHT-150, BLUE, False)
car_oponent = graphics.Car(SCREEN_WIDTH/2-75, SCREEN_HEIGHT-150, RED, True)

#create countdown lights with random 2-5s delay
starting_lights = graphics.StartingLights(SCREEN_WIDTH/2, 100)

# calculate dashboard position
dashboard = graphics.Dashboard(SCREEN_WIDTH/2, SCREEN_HEIGHT-120)
lastTimeGearChange = 0
FalseStart = False

while True:   
    lastTimeGearChange += 1  
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()      
            sys.exit()
    # countdown lights
    while starting_lights.state < 5:
        road.draw(menu_window, car.x)
        car.draw(menu_window)
        car_oponent.draw(menu_window)
        dashboard.draw(menu_window, car.engine.current_rpm, car.speed, car.engine.gear)
        starting_lights.draw(menu_window)
        pygame.display.update()
        FramePerSec.tick(FPS)
        # check for false start
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()      
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("False start!")
                    FalseStart = True
                    break
        if FalseStart:
            break
    if FalseStart:
        break
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            if lastTimeGearChange > 10:
                car.gearUp()
                lastTimeGearChange = 0
        if event.key == pygame.K_DOWN:
            if lastTimeGearChange > 10:
                car.gearDown()
                lastTimeGearChange = 0

    road.draw(menu_window, car.x)
    car.update_phisics()
    car_oponent.update_phisics()
    car.draw(menu_window)
    car_oponent.draw(menu_window)
    dashboard.draw(menu_window, car.engine.current_rpm, car.speed, car.engine.gear)
    # print car position as remaining distance to the destination
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render('Distance to Politechnika Poznańska: ' + str(round(car.x, 2)) + 'm, bieg: ' + str(car.engine.gear), False, (0, 0, 0))
    menu_window.blit(textsurface,(0,0))
    pygame.display.update()
    FramePerSec.tick(FPS)

if FalseStart:
    pygame.draw.rect(menu_window, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    print("You are late to the classes!")
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('False start!', True, (0, 0, 0))
    text_rect = textsurface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    menu_window.blit(textsurface, text_rect)

    textsurface = myfont.render('Press any key to exit', True, (0, 0, 0))
    text_rect = textsurface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    menu_window.blit(textsurface, text_rect)
    pygame.display.update()
    # wait 5s
    time.sleep(5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                break
            if event.type == QUIT:
                pygame.quit()      
                sys.exit()
        if event.type == pygame.KEYDOWN:
            break
        FramePerSec.tick(FPS)