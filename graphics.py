import pygame
from pygame.locals import *
import random
pygame.init()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, color, wheels_color=BLACK):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50
        self.cabin_width = 80
        self.cabin_height = 30
        self.wheels_color = wheels_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.circle(surface, self.wheels_color, (self.x + 10, self.y + self.height), 10)
        pygame.draw.circle(surface, self.wheels_color, (self.x + self.width - 10, self.y + self.height), 10)
        #pygame.draw.rect(surface, WHITE, (self.x + 20, self.y + 10, self.width - 40, self.height - 20))
        #pygame.draw.circle(surface, BLACK, (self.x + 30, self.y + self.height // 2), 10)
        #pygame.draw.polygon(surface, self.color, [(self.x + 20, self.y - self.height), (self.x + self.width - 20, self.y - self.height), (self.x + self.width, self.y), (self.x, self.y)])
        pygame.draw.rect(surface, self.color, (self.x + (self.width - self.cabin_width) // 2, self.y - self.height + 5, self.cabin_width, self.cabin_height), border_radius=5)
        pygame.draw.polygon(surface, self.color, [(self.x + (self.width - self.cabin_width) // 2, self.y - self.height + 5), (self.x + (self.width + self.cabin_width) // 2, self.y - self.height + 5), (self.x + self.width, self.y)])

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.x -= 5
        if pressed_keys[K_RIGHT]:
            self.x += 5

class Road(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.terrain_color = color
        self.width = 400
        self.height = 600
        self.alpha = 0.005  # Decreased alpha value for smoother slopes
        self.shape = self.generate_shape()

    def generate_shape(self):
        shape = []
        for i in range(self.width):
            height = random.randint(0, self.height)
            shape.append(height)
        shape = self.apply_low_pass_filter(shape, self.alpha)
        return shape
    
    def apply_low_pass_filter(self, shape, alpha=0.2):
        filtered_shape = []
        filtered_shape.append(shape[0])
        for i in range(1, len(shape)):
            filtered_height = alpha * shape[i] + (1 - alpha) * filtered_shape[i-1]
            filtered_shape.append(filtered_height)
        return filtered_shape
    
    def draw(self, surface):
        pygame.draw.polygon(surface, self.terrain_color, self.get_polygon_points(), 0)
        
    def get_polygon_points(self):
        points = []
        for i in range(self.width):
            points.append((self.x + i, self.y + self.height - self.shape[i]))
        points.append((self.x + self.width, self.y + self.height))
        points.append((self.x, self.y + self.height))
        return points

    def move(self, direction):
        if direction == "left":
            self.x -= 5
        elif direction == "right":
            self.x += 5
