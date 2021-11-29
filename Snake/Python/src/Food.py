import pygame
import random
from config import food_source, display_size, square_size

class Food:
    def __init__(self, parent_screen):
        self.image = pygame.image.load(food_source).convert_alpha()
        self.parent_screen = parent_screen
        self.x = random.randint(0, display_size[0]-1)*square_size
        self.y = random.randint(0, display_size[1]-1)*square_size
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, display_size[0]-1)*square_size
        self.y = random.randint(0, display_size[1]-1)*square_size