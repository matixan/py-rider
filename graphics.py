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
    def __init__(self, x, y, color, wheels_color=BLACK):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 25
        self.cabin_width = 50
        self.cabin_height = 10
        self.wheels_color = wheels_color
        self.max_speed = 50 # Maximum speed value in km/h
        self.max_acc = 0.5 # Maximum acceleration value in m/s^2
        self.speed = 0
        self.acc = 0
        self.weight = 1000 # Weight of the car in kg
        self.traction = 0.70 # Traction coefficient in range 0-1
        self.engine = Engine(100)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.circle(surface, self.wheels_color, (self.x + 10, self.y + self.height), 10)
        pygame.draw.circle(surface, self.wheels_color, (self.x + self.width - 10, self.y + self.height), 10)
        pygame.draw.rect(surface, self.color, (self.x + (self.width - self.cabin_width) // 2, self.y - self.height + 5, self.cabin_width, self.cabin_height), border_radius=5)
        pygame.draw.polygon(surface, self.color, [(self.x + (self.width - self.cabin_width) // 2, self.y - self.height + 5), (self.x + (self.width + self.cabin_width) // 2, self.y - self.height + 5), (self.x + self.width, self.y)])
    
    def gearUp(self):
        if self.engine.gear < 6:
            self.engine.gear += 1
            print("Gear up: ", self.engine.gear)
    def gearDown(self):
        if self.engine.gear > 1:
            self.engine.gear -= 1
            print("Gear down: ", self.engine.gear)

    def apply_accelerate(self):
        self.acc += 0.1/(self.speed+1)
        if self.acc > self.max_acc:
            self.acc = self.max_acc

    def update_phisics(self):
        self.speed += self.acc
        if self.speed < 0:
            self.speed = 0
        if self.engine.gear != 0:
            self.engine.current_rpm = self.speed * 1000 / (0.6 * math.pi * 0.3)

        if self.speed >= self.max_speed:
            self.speed = self.max_speed
        elif self.speed <= -self.max_speed+20:
            self.speed = -self.max_speed+20
    def engine_idle(self):
        # when engine is neither accelerating nor braking, it should decelerate slightly
        if self.acc != 0:
            self.acc -= 0.01
            if self.acc < 0:
                self.acc = 0
    def update_position(self):
        self.x += self.speed/3.6 # speed is in km/h, we need to convert it to m/s

class Engine(pygame.sprite.Sprite):
    def __init__(self, power):
        super().__init__()
        self.gear=0
        self.power = power # Power of the engine in KW
        self.torque = 300 # Torque of the engine in Nm
        self.current_rpm = 0 # Current revolutions per minute
        self.idle_rpm = 900 # Revolutions per minute
        self.max_rpm = 8000 # Maximum revolutions per minute

class Road(pygame.sprite.Sprite):
    def __init__(self, width, x, y, color):
        self.x = x # metry
        self.y = y # offset
        self.terrain_color = color
        self.width = width
        self.alpha = 0.005  # Decreased alpha value for smoother slopes
        self.shape = self.generate_shape()

    def generate_shape(self):
        shape = []
        for i in range(self.width):
            shape.append(self.y * math.sin(self.alpha * i + self.x) + self.y)
        return shape
    
    def draw(self, surface, x, y):
        pygame.draw.polygon(surface, self.terrain_color, [(0, self.y), (0, self.shape[0]), (self.width, self.shape[-1]), (self.width, self.y)])


class Dashboard(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.radius = 100
        self.rpm = 0
        self.speed = 23
        self.max_rpm = 8000
        self.max_speed = 150

    def draw(self, surface, rpm, speed):
        pygame.draw.circle(surface, GREY, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 5)
        pygame.draw.circle(surface, GREY, (self.x+250, self.y), self.radius)
        pygame.draw.circle(surface, self.color, (self.x+250, self.y), self.radius, 5)
        self.draw_needle(surface, self.x, self.y, self.rpm, self.max_rpm, self.radius * 0.8, self.radius * 0.05)
        self.draw_needle(surface, self.x+250, self.y, self.speed, self.max_speed, self.radius * 0.6, self.radius * 0.05)
        self.draw_label(surface, "RPM", self.x, self.y+75)
        self.draw_label(surface, "SPEED", self.x+250, self.y+75)
        self.draw_value(surface, round(rpm), self.x, self.y-75)
        self.draw_value(surface, round(speed), self.x+250, self.y-75)
        self.draw_axis(surface, self.x, self.y, self.radius, 10, -45, 225)
        self.draw_axis(surface, self.x+250, self.y, self.radius, 10, -45, 225)


    def draw_needle(self, surface, x, y, value, max_value, length, thickness):
        angle = 180 - value / max_value * 180
        end_x = x + length * math.cos(math.radians(angle))
        end_y = y - length * math.sin(math.radians(angle))
        pygame.draw.line(surface, WHITE, (x, y), (end_x, end_y), int(thickness))
        surface.blit(surface, (end_x, end_y))

    def draw_label(self, surface, label, x, y):
        font = pygame.font.Font(None, 20)
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

    def draw_value(self, surface, value, x, y):
        font = pygame.font.Font(None, 20)
        text = font.render(str(value), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

    # draws small lines around perimeter of the circle
    def draw_axis(self, surface, x, y, radius, num_lines, min_phi, max_phi):
        for i in range(num_lines):
            phi = min_phi + i * (max_phi - min_phi) / num_lines
            start_x = x + (radius - 10) * math.cos(math.radians(phi))
            start_y = y - (radius - 10) * math.sin(math.radians(phi))
            end_x = x + radius * math.cos(math.radians(phi))
            end_y = y - radius * math.sin(math.radians(phi))
            pygame.draw.line(surface, WHITE, (start_x, start_y), (end_x, end_y), 2)