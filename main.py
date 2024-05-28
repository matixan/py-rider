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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
MENU_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
menu_window = pygame.display.set_mode(MENU_SIZE)
menu_window.fill(WHITE)
pygame.display.set_caption("PyRider - Politechnika Poznańska Edition")
icon = pygame.image.load('data/PP_logo_RGB.png')
pygame.display.set_icon(icon)
gamePaused = False

# create car
car = graphics.Car(175, 200, RED)

# create road
road = graphics.Road(SCREEN_WIDTH,0, 0, GREEN)

# create dashboard on the bottom of the screen
dashboard = graphics.Dashboard(500, 600, BLACK)

while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()      
            sys.exit()
    #handling pauzy
    while gamePaused:
        pygame.display.update()
        FramePerSec.tick(FPS)
        pygame.draw.label(menu_window)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gamePaused = False
                    print("Game unpaused")

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
            car.apply_brake()
            print("Braking, acc: ", round(car.acc, 4), "speed: ", round(car.speed, 4), "rpm: ", round(car.engine.current_rpm,4), "brake: ", round(car.brake,4))
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
            car.apply_accelerate()
            print("Accelerating, acc: ", round(car.acc, 4), "speed: ", round(car.speed, 4), "rpm: ", round(car.engine.current_rpm,4), "brake: ", round(car.brake,4))
        elif event.key == pygame.K_p:
            gamePaused = True
            print("Game paused")

    car.engine_idle()
    print("Idle, acc: ", round(car.acc, 4), "speed: ", round(car.speed, 4), "rpm: ", round(car.engine.current_rpm,4), "brake: ", round(car.brake,4))
    menu_window.fill(WHITE)
    car.update_phisics()
    car.update_position()
    car.draw(menu_window)
    road.draw(menu_window, car.x, car.y)
    dashboard.draw(menu_window, car.engine.current_rpm, car.speed)
    # print car position as remaining distance to the destination
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render('Distance to Politechnika Poznańska: ' + str(round(car.x, 2)) + 'm, bieg: ' + str(car.engine.gear), False, (0, 0, 0))
    menu_window.blit(textsurface,(0,0))
    pygame.display.update()
    FramePerSec.tick(FPS)