import pygame
from config import block_source, square_size, fill_color, isWallAnEnd, display_size

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(block_source).convert_alpha()
        self.x = [square_size]*length
        self.y = [square_size]*length
        self.direction = 'd'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        self.parent_screen.fill(fill_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_left(self):
        self.direction = 'l'
    def move_right(self):
        self.direction = 'r'
    def move_up(self):
        self.direction = 'u'
    def move_down(self):
        self.direction = 'd'
    
    def move_snake(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if (self.direction == 'l'):
            if not isWallAnEnd and self.x[0]==0:
                    self.x[0] = (display_size[0]-1)*square_size
            else:
                self.x[0] -= square_size
        elif (self.direction == 'r'):
            if not isWallAnEnd and self.x[0]==(display_size[0]-1)*square_size:
                    self.x[0] = 0
            else:
                self.x[0] += square_size
        elif (self.direction == 'u'):
            if not isWallAnEnd and self.y[0]==0:
                self.y[0] = (display_size[1]-1)*square_size
            else:
                self.y[0] -= square_size
        elif (self.direction == 'd'):
            if not isWallAnEnd and self.y[0]==(display_size[1]-1)*square_size:
                self.y[0] = 0
            else:
                self.y[0] += square_size
        self.draw()