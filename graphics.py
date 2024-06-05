import pygame
from pygame.locals import *
import random
import math
pygame.init()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, color, opponent=False):
        super().__init__()
        self.bot = opponent
        self.x = x
        self.y = y
        self.distance = 0
        self.color = color
        self.width = 50
        self.height = 100
        self.max_speed = 150 # Maximum speed value in km/h
        self.speed = 0
        self.acc = 0
        self.weight = 1000 # Weight of the car in kg
        if self.bot: self.engine = Engine(80) # you can beat him
        else: self.engine = Engine(100)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=8)

    def gearUp(self):
        if self.engine.gear < 6:
            self.engine.gear += 1
            print("Gear up: ", self.engine.gear)
            if self.engine.gear != 1:
                self.engine.current_rpm /= 2
    def gearDown(self):
        if self.engine.gear >= 1:
            self.engine.gear -= 1
            print("Gear down: ", self.engine.gear)
            if self.engine.gear != 1:
                self.engine.current_rpm *= 2

    def update_phisics(self):
        # Calculate acceleration force
        if self.engine.gear == 0:
            self.engine.current_rpm = self.engine.idle_rpm
        else:
            # Power increases with RPM up to a point, then decreases based on the power curve
            power = self.engine.power_curve * self.engine.power
            print("Power: ", power)
            force = power * 0.7 # 70% of the power is used to move the car
            self.acc = force / self.weight
            # Calculate RPM
            self.engine.current_rpm = self.engine.current_rpm + self.acc * 1000
            if self.engine.current_rpm > self.engine.max_rpm:
                # Engine is limited to the maximum RPM, so the speed is not increasing anymore
                self.engine.current_rpm = self.engine.max_rpm
                self.speed = self.engine.max_rpm * self.engine.gear * 0.5 / 1000
            # Calculate speed
            if self.speed < 0:
                self.speed = 0
            if self.speed > self.max_speed:
                self.speed = self.max_speed
            # Calculate distance
            self.distance += self.speed / 3600 # 1 hour = 3600 seconds
            
        print("Speed: ", self.speed, "Distance: ", self.distance, "RPM: ", self.engine.current_rpm, "Acc: ", self.acc)


        

class Engine(pygame.sprite.Sprite):
    def __init__(self, power):
        super().__init__()
        self.gear=0
        self.power = power # Power of the engine in KW
        self.torque = 300 # Torque of the engine in Nm
        self.idle_rpm = 900 # Revolutions per minute
        self.current_rpm = self.idle_rpm # Current revolutions per minute
        self.max_rpm = 8000 # Maximum revolutions per minute
        self.power_curve = self.calculate_power_curve()

    def calculate_power_curve(self):
        function = 0.5 * self.current_rpm/1000 - 0.06 * (self.current_rpm/1000)**2 -0.2
        return function
class Road(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
    # from bottom to top
    def draw(self, surface, distance):
        # road is grey
        pygame.draw.rect(surface, GREY, (0, 0, self.width, self.height))
        # road lines are white and dashed, lines are moving from top to bottom
        for i in range(-50, self.height + 50, 100):
            pygame.draw.line(surface, WHITE, (self.width//2, i+distance%100), (self.width//2, i+50+distance%100), 5)
        # on the left and right side of the road there are green fields
        pygame.draw.rect(surface, GREEN, (0, 0, self.width//2-100, self.height))
        pygame.draw.rect(surface, GREEN, (self.width//2+100, 0, self.width//2-100, self.height))
        # at the end of the road there is a finish line
        if distance > 1000:
            pygame.draw.rect(surface, WHITE, (self.width//2-100, 0, 200, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("FINISH", True, BLACK)
            text_rect = text.get_rect(center=(self.width//2, 25))
            surface.blit(text, text_rect)

class Dashboard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x-225
        self.y = y
        self.radius = 100
        self.old_rpm = 0
        self.max_rpm = 8000
        self.max_speed = 150

    def draw(self, surface, rpm, speed, gear):
        # draw speedometer on the left side and tachometer on the right side
        pygame.draw.circle(surface, GREY, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius, 5)
        pygame.draw.circle(surface, GREY, (self.x+450, self.y), self.radius)
        # draw not optimal rpm range in red from 6000 to 8000 using arc
        pygame.draw.arc(surface, RED, (self.x+450-self.radius, self.y-self.radius, 200, 200), math.radians(40), math.radians(80), 40)
        pygame.draw.arc(surface, GREEN, (self.x+450-self.radius, self.y-self.radius, 200, 200), math.radians(80), math.radians(110), 40)
        pygame.draw.circle(surface, BLACK, (self.x+450, self.y), self.radius, 5)
        # draw small labels for each 1000 rpm and 20 km/h
        for i in range(0, 9):
            angle = (i/8) * 180-225
            reduced_radius = self.radius * 0.8  # Reduce the radius to draw inside the circle
            font = pygame.font.Font(None, 24)

            x = self.x + reduced_radius * math.cos(math.radians(angle))
            y = self.y + reduced_radius * math.sin(math.radians(angle))
            text = font.render(str(i*20), True, BLACK)
            text_rect = text.get_rect(center=(int(x), int(y)))
            surface.blit(text, text_rect)
                
            x = self.x + 450 + reduced_radius * math.cos(math.radians(angle))
            y = self.y + reduced_radius * math.sin(math.radians(angle))
            text = font.render(str(i*1), True, BLACK)
            text_rect = text.get_rect(center=(int(x), int(y)))
            surface.blit(text, text_rect)
        # draw labels
        font = pygame.font.Font(None, 36)
        text = font.render("Speed", True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y-25))
        surface.blit(text, text_rect)
        # draw speedometer needle
        angle = (speed/self.max_speed) * 180-225 # simple fix for the needle starting position
        x = self.x
        y = self.y
        x1 = x + self.radius * math.cos(math.radians(angle))
        y1 = y + self.radius * math.sin(math.radians(angle))
        pygame.draw.line(surface, WHITE, (x, y), (x1, y1), 5)
        # draw gear indicator
        text = font.render("Gear: " + str(gear), True, BLACK)
        text_rect = text.get_rect(center=(self.x+450, self.y+25))
        surface.blit(text, text_rect)
        # draw tachometer needle
        text = font.render("RPM", True, BLACK)
        text_rect = text.get_rect(center=(self.x+450, self.y-25))
        surface.blit(text, text_rect)
        # smooth needle movement
        difference = rpm - self.old_rpm
        if difference > 200:
            difference = 200
        elif difference < -200:
            difference = -200
        self.old_rpm += difference
        angle = (self.old_rpm/self.max_rpm) * 180-225
        x = self.x+450
        y = self.y
        x1 = x + self.radius * math.cos(math.radians(angle))
        y1 = y + self.radius * math.sin(math.radians(angle))
        pygame.draw.line(surface, WHITE, (x, y), (x1, y1), 5)

class StartingLights(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x-125
        self.y = y
        self.radius = 20
        self.lights = [RED, RED, RED, RED, RED]
        self.delay = random.randint(2, 5) * 100
        self.last_time = 0
        self.current_time = 0
        self.state = 0

    def draw(self, surface):
        #draw starting lights background
        pygame.draw.rect(surface, BLACK, (self.x, self.y-25, 5*50, 50))
        # draw 5 lights
        for i in range(5):
            pygame.draw.circle(surface, self.lights[i], (self.x+i*50+25, self.y), self.radius)
        if self.state == 0:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_time > self.delay:
                self.last_time = self.current_time
                self.state += 1
        elif self.state == 1:
            self.lights[0] = GREEN
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_time > 1000:
                self.last_time = self.current_time
                self.state += 1
        elif self.state == 2:
            self.lights[1] = GREEN
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_time > 1000:
                self.last_time = self.current_time
                self.state += 1
        elif self.state == 3:
            self.lights[2] = GREEN
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_time > 1000:
                self.last_time = self.current_time
                self.state += 1
        elif self.state == 4:
            self.lights[3] = GREEN
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_time > 1000:
                self.last_time = self.current_time
                self.state += 1
        elif self.state == 5:
            self.lights[4] = GREEN
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_time > 1000:
                self.last_time = self.current_time
                self.state += 1