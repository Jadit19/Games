import pygame
import os, sys
import csv
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from src.Button import Button
from config import *

pygame.init()

LOWER_MARGIN = 100
SIDE_MARGIN = 300
MAX_COLS = COLS
GREEN = (144,201,120)
WHITE = (255,255,255)
RED = (200,25,25)

screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption("Level Editor")
clock = pygame.time.Clock()
world_data = []
for r in range(ROWS):
    world_row = [-1]*MAX_COLS
    world_data.append(world_row)
for tile in range(0, MAX_COLS):
    world_data[ROWS-1][tile] = 0

#! Game Variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_tile = 0
level = 0
font = pygame.font.SysFont("Futura", 30)

#! Loading images
pine1_img = pygame.image.load("../img/background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("../img/background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("../img/background/mountain.png").convert_alpha()
sky_img = pygame.image.load("../img/background/sky_cloud.png").convert_alpha()
save_img = pygame.image.load("../img/save_btn.png").convert_alpha()
load_img = pygame.image.load("../img/load_btn.png").convert_alpha()
img_list = []
button_list = []
button_col = 0
button_row = 0
for i in range(TILE_TYPES):
    img = pygame.image.load(f'../img/tile/{i}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
for i in range(len(img_list)):
    tile_button = Button(SCREEN_WIDTH+(75*button_col)+50, 75*button_row+50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0
save_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT+LOWER_MARGIN-70, save_img, 1)
load_button = Button(SCREEN_WIDTH//2+200, SCREEN_HEIGHT+LOWER_MARGIN-70, load_img, 1)

def draw_bg():
    global scroll
    screen.fill(GREEN)
    for i in range(4):
        width = sky_img.get_width()
        screen.blit(sky_img, ((i*width)-scroll*0.5,0))
        screen.blit(mountain_img, ((i*width)-scroll*0.6, SCREEN_HEIGHT-mountain_img.get_height()-300))
        screen.blit(pine1_img, ((i*width)-scroll*0.7, SCREEN_HEIGHT-pine1_img.get_height()-150))
        screen.blit(pine2_img, ((i*width)-scroll*0.8, SCREEN_HEIGHT-pine2_img.get_height()))
    if save_button.draw(screen):
        with open(f'../Levels/Level_{level}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for r in world_data:
                writer.writerow(r)
    if load_button.draw(screen):
        scroll = 0
        with open(f'../Levels/Level_{level}.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

def draw_grid():
    for c in range(MAX_COLS+1):
        pygame.draw.line(screen, WHITE, (c*TILE_SIZE-scroll,0), (c*TILE_SIZE-scroll, SCREEN_HEIGHT))
    for r in range(ROWS+1):
        pygame.draw.line(screen, WHITE, (0, r*TILE_SIZE), (SCREEN_WIDTH, r*TILE_SIZE))

def draw_side_bar():
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    button_count = 0
    global current_tile
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x*TILE_SIZE-scroll, y*TILE_SIZE))

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_all():
    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-90)
    draw_text('Press up or down to change level', font, WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-70)
    draw_side_bar()

def insert_new_tile():
    pos = pygame.mouse.get_pos()
    x = int((pos[0]+scroll) // TILE_SIZE)
    y = int((pos[1]) // TILE_SIZE)
    global current_tile

    if pos[0]<SCREEN_WIDTH and pos[1]<SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        elif pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1


run = True
while run:
    clock.tick(FPS)
    draw_all()

    if scroll_left and scroll>0:
        scroll -= 5*scroll_speed
    if scroll_right and scroll<MAX_COLS*TILE_SIZE-SCREEN_WIDTH:
        scroll += 5*scroll_speed

    insert_new_tile()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_LEFT:
                scroll_left = True
            elif event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN:
                if level > 0:
                    level -= 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            elif event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()