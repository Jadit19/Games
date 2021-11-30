import pygame
from config import block_source, square_size, fill_color, isWallAnEnd, display_size, ext

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.x = [square_size]*length
        self.y = [square_size]*length
        self.block_type = [square_size]*(length-2)
        self.direction = 'd'

        self.head_u = pygame.image.load(block_source + 'head_u' + ext).convert_alpha()
        self.head_d = pygame.image.load(block_source + 'head_d' + ext).convert_alpha()
        self.head_l = pygame.image.load(block_source + 'head_l' + ext).convert_alpha()
        self.head_r = pygame.image.load(block_source + 'head_r' + ext).convert_alpha()

        self.body_v = pygame.image.load(block_source + 'body_v' + ext).convert_alpha()
        self.body_h = pygame.image.load(block_source + 'body_h' + ext).convert_alpha()
        
        self.tail_u = pygame.image.load(block_source + 'tail_u' + ext).convert_alpha()
        self.tail_d = pygame.image.load(block_source + 'tail_d' + ext).convert_alpha()
        self.tail_l = pygame.image.load(block_source + 'tail_l' + ext).convert_alpha()
        self.tail_r = pygame.image.load(block_source + 'tail_r' + ext).convert_alpha()

        self.bent_tl = pygame.image.load(block_source + 'bent_tl' + ext).convert_alpha()
        self.bent_tr = pygame.image.load(block_source + 'bent_tr' + ext).convert_alpha()
        self.bent_bl = pygame.image.load(block_source + 'bent_bl' + ext).convert_alpha()
        self.bent_br = pygame.image.load(block_source + 'bent_br' + ext).convert_alpha()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        self.block_type.append(-1)

    def choose_head_block(self):
        if self.direction == 'u':
            return self.head_u
        elif self.direction == 'd':
            return self.head_d
        elif self.direction == 'l':
            return self.head_l
        else:
            return self.head_r
    
    def choose_tail_block(self):
        if not isWallAnEnd:
            if self.y[self.length-2]==0 and self.y[self.length-1]==((display_size[1]-1)*square_size):
                return self.tail_d
            elif self.y[self.length-2]==((display_size[1]-1)*square_size) and self.y[self.length-1]==0:
                return self.tail_u
            elif self.x[self.length-2]==0 and self.x[self.length-1]==((display_size[0]-1)*square_size):
                return self.tail_r
            elif self.x[self.length-2]==((display_size[0]-1)*square_size) and self.x[self.length-1]==0:
                return self.tail_l
            

        if self.x[self.length-2]==self.x[self.length-1]:
            if self.y[self.length-2]>self.y[self.length-1]:
                return self.tail_d
            else:
                return self.tail_u
        else:
            if self.x[self.length-2]>self.x[self.length-1]:
                return self.tail_r
            else:
                return self.tail_l

    def choose_first_body_block(self):
        if not isWallAnEnd:
            if self.y[0]==self.y[1]:
                if self.x[0]==((display_size[0]-1)*square_size) and self.x[1]==0:
                    if self.y[1]-self.y[2]==square_size:
                        return self.bent_bl
                    elif self.y[1]==((display_size[1]-1)*square_size) and self.y[2]==0:
                        return self.bent_bl
                    elif self.y[2]-self.y[1]==square_size:
                        return self.bent_tl
                    elif self.y[1]==0 and self.y[2]==((display_size[1]-1)*square_size):
                        return self.bent_tl
                elif self.x[0]==0 and self.x[1]==((display_size[0]-1)*square_size):
                    if self.y[1]-self.y[2]==square_size:
                        return self.bent_br
                    elif self.y[1]==((display_size[1]-1)*square_size) and self.y[2]==0:
                        return self.bent_br
                    elif self.y[2]-self.y[1]==square_size:
                        return self.bent_tr
                    elif self.y[1]==0 and self.y[2]==((display_size[1]-1)*square_size):
                        return self.bent_tr
                elif self.y[0]==0 and self.y[2]==((display_size[1]-1)*square_size):
                    if self.x[0]-self.x[1]==square_size:
                        return self.bent_tr
                    elif self.x[1]-self.x[1]==square_size:
                        return self.bent_tl
                elif self.y[0]==((display_size[1]-1)*square_size) and self.y[2]==0:
                    if self.x[0]-self.x[1]==square_size:
                        return self.bent_br
                    elif self.x[1]-self.x[0]==square_size:
                        return self.bent_bl
            elif self.x[0]==self.x[1]:
                if self.y[0]==((display_size[1]-1)*square_size) and self.y[1]==0:
                    if self.x[1]-self.x[2]==square_size:
                        return self.bent_tl
                    elif self.x[1]==((display_size[0]-1)*square_size) and self.x[2]==0:
                        return self.bent_tl
                    elif self.x[2]-self.x[1]==square_size:
                        return self.bent_tr
                    elif self.x[1]==0 and self.x[2]==((display_size[0]-1)*square_size):
                        return self.bent_tr
                elif self.y[0]==0 and self.y[1]==((display_size[1]-1)*square_size):
                    if self.x[1]-self.x[2]==square_size:
                        return self.bent_bl
                    elif self.x[1]==((display_size[0]-1)*square_size) and self.x[2]==0:
                        return self.bent_bl
                    elif self.x[2]-self.x[1]==square_size:
                        return self.bent_br
                    elif self.x[1]==0 and self.x[2]==((display_size[0]-1)*square_size):
                        return self.bent_br
                elif self.x[0]==0 and self.x[2]==((display_size[0]-1)*square_size):
                    if self.y[0]-self.y[1]==square_size:
                        return self.bent_bl
                    elif self.y[1]-self.y[0]==square_size:
                        return self.bent_tl
                elif self.x[0]==((display_size[0]-1)*square_size) and self.x[2]==0:
                    if self.y[0]-self.y[1]==square_size:
                        return self.bent_br
                    elif self.y[1]-self.y[0]==square_size:
                        return self.bent_tr

        if self.x[0]==self.x[2]:
            return self.body_v
        elif self.y[0]==self.y[2]:
            return self.body_h
        elif self.x[0]>self.x[2]:
            if self.y[0]>self.y[2]:
                if self.x[0]==self.x[1]:
                    return self.bent_bl
                else:
                    return self.bent_tr
            else:
                if self.x[0]==self.x[1]:
                    return self.bent_tl
                else:
                    return self.bent_br
        else:
            if self.y[0]>self.y[2]:
                if self.x[0]==self.x[1]:
                    return self.bent_br
                else:
                    return self.bent_tl
            else:
                if self.x[0]==self.x[1]:
                    return self.bent_tr
                else:
                    return self.bent_bl
    
    def draw(self):
        self.parent_screen.fill(fill_color)
        self.parent_screen.blit(self.choose_head_block(), (self.x[0], self.y[0]))
        if self.length>1:
            self.parent_screen.blit(self.choose_tail_block(), (self.x[self.length-1], self.y[self.length-1]))
            if self.length>2:
                self.block_type[0] = self.choose_first_body_block()
                self.parent_screen.blit(self.block_type[0], (self.x[1], self.y[1]))
                if self.length>3:
                    for i in range(2, self.length-1):
                        self.parent_screen.blit(self.block_type[i-1], (self.x[i], self.y[i]))

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
        if (self.length>3):
            for i in range(self.length-3, 0, -1):
                self.block_type[i] = self.block_type[i-1]
        
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