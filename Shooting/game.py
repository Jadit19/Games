import pygame
import os
import random
import csv
from config import *
from src.ItemBox import ItemBox
from src.HealthBar import HealthBar
from src.Explosion import Explosion
from src.Extras import Decoration, Water, Exit
from src.Button import Button

#! Initializing
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting Game")
font = pygame.font.SysFont("Futura", 30)
clock = pygame.time.Clock()

moving_left = False
moving_right = False
shoot = False
throw = False
grenade_thrown = False
screen_scroll = 0
bg_scroll = 0
run = True
start_game = False

#! Loading Images
pine1_img = pygame.image.load("./img/background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("./img/background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("./img/background/mountain.png").convert_alpha()
sky_img = pygame.image.load("./img/background/sky_cloud.png").convert_alpha()
bullet_img = pygame.image.load("./img/icons/bullet.png").convert_alpha()
grenade_img = pygame.image.load("./img/icons/grenade.png").convert_alpha()
health_box = pygame.image.load('./img/icons/health_box.png').convert_alpha()
ammo_box = pygame.image.load('./img/icons/ammo_box.png').convert_alpha()
grenade_box = pygame.image.load('./img/icons/grenade_box.png').convert_alpha()
start_img = pygame.image.load("./img/start_btn.png").convert_alpha()
exit_img = pygame.image.load("./img/exit_btn.png").convert_alpha()
restart_img = pygame.image.load("./img/restart_btn.png").convert_alpha()
img_list = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'./img/Tile/{i}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
start_btn = Button(SCREEN_WIDTH//2-130, SCREEN_HEIGHT//2-150, start_img, 1)
exit_btn = Button(SCREEN_WIDTH//2-110, SCREEN_HEIGHT//2+50, exit_img, 1)
restart_btn = Button(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2-50, restart_img, 2)

#! Block groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


def draw_bg():
    screen.fill((144,201,120))
    w = sky_img.get_width()
    for i in range(5):
        screen.blit(sky_img, (i*w-bg_scroll*0.5, 0))
        screen.blit(mountain_img, (i*w-bg_scroll*0.6, SCREEN_HEIGHT-mountain_img.get_height()-300))
        screen.blit(pine2_img, (i*w-bg_scroll*0.7, SCREEN_HEIGHT-pine2_img.get_height()-80))
        screen.blit(pine1_img, (i*w-bg_scroll*0.8, SCREEN_HEIGHT-pine1_img.get_height()))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def load_level(lvl):
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    data = []
    for r in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    with open(f'./Levels/Level_{lvl}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                data[x][y] = int(tile)
    return data

def throw_grenade():
    if player.grenades > 0:
        grenade = Grenade(player.rect.centerx + player.rect.size[0]*0.5*player.direction,
                                player.rect.centery - player.rect.size[1]*0.5,
                                player.direction)
        grenade_group.add(grenade)
        player.grenades -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right<0 or self.rect.left>SCREEN_WIDTH:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.living:
                self.kill()
                player.health -= 5
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.living:
                    self.kill()
                    enemy.health -= 25


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.timer = 50
        self.vel_y = -11

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.rect.width, self.rect.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.rect.width, self.rect.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                else:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            if abs(self.rect.centerx-player.rect.centerx)<TILE_SIZE*2 and abs(self.rect.y - player.rect.centery)<TILE_SIZE*2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx-enemy.rect.centerx)<TILE_SIZE*2 and abs(self.rect.y - enemy.rect.centery)<TILE_SIZE*2:
                    enemy.health -= 50


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.living = True
        self.frame_index = 0
        self.action = 0
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health

        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)

        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        self.animation_list = []
        for ani in animation_types:
            temp_list = []
            for i in range(len(os.listdir(f'./img/{self.char_type}/{ani}'))):
                img = pygame.image.load(f'./img/{self.char_type}/{ani}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def shoot(self):
        if self.shoot_cooldown==0 and self.ammo>0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + self.rect.size[0]*0.65*self.direction, self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
    
    def ai(self):
        if self.living and player.living:
            self.vision.center = (self.rect.centerx + 75*self.direction, self.rect.centery)
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot()
            else:
                if not self.idling and random.randint(1,100)==1:
                    self.update_action(0)
                    self.idling = True
                    self.idling_counter = 100
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter = 0
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        self.rect.x += screen_scroll

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[3])-1
            else:
                self.frame_index = 0
    
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self, ml, mr):
        screen_scroll = 0
        dx = 0
        dy = 0
        if ml:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        elif mr:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                else:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        if self.char_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
        if player.living:
            self.rect.x += dx
            self.rect.y += dy
        level_complete = False
        if self.char_type == 'player':
            if pygame.sprite.spritecollide(self, water_group, False):
                self.health = 0
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True
            if self.rect.bottom > SCREEN_HEIGHT:
                self.health = 0
            if (self.rect.right>SCREEN_WIDTH-SCROLL_THRESH and bg_scroll<world.level_length*TILE_SIZE-SCREEN_WIDTH) or (self.rect.left<SCROLL_THRESH and bg_scroll>abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll, level_complete
    
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown>0:
            self.shoot_cooldown -= 1

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.living = False
            self.update_action(3)
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile < 9:                                # Dirt
                        self.obstacle_list.append(tile_data)
                    elif tile < 11:                             # Water
                        water = Water(img, x*TILE_SIZE, y*TILE_SIZE)
                        water_group.add(water)
                    elif tile < 15:
                        decoration = Decoration(img, x*TILE_SIZE, y*TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:                            # Player
                        player = Soldier('player', x*TILE_SIZE, y*TILE_SIZE, 1, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health, screen)
                    elif tile == 16:                            # Enemy
                        enemy = Soldier('enemy', x*TILE_SIZE, y*TILE_SIZE, 1, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:                            # Ammo Box
                        item_box = ItemBox("Ammo", x*TILE_SIZE, y*TILE_SIZE, ammo_box)
                        item_box_group.add(item_box)
                    elif tile == 18:                            # Grenade Box
                        item_box = ItemBox("Grenade", x*TILE_SIZE, y*TILE_SIZE, grenade_box)
                        item_box_group.add(item_box)
                    elif tile == 19:                            # Health Box
                        item_box = ItemBox("Health", x*TILE_SIZE, y*TILE_SIZE, health_box)
                        item_box_group.add(item_box)
                    elif tile == 20:                            # Exit
                        exit_ = Exit(img, x*TILE_SIZE, y*TILE_SIZE)
                        exit_group.add(exit_)
        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        draw_text('AMMO: ', font, (255,255,255), 10, 35)
        for i in range(player.ammo):
            screen.blit(bullet_img, (90 + i*10, 40))
        draw_text('GRENADES: ', font, (255,255,255), 10, 60)
        for i in range(player.grenades):
            screen.blit(grenade_img, (140 + i*15, 60))
        health_bar.draw(player.health)
        item_box_group.update(player, screen_scroll)
        bullet_group.update()
        grenade_group.update()
        explosion_group.update(screen_scroll)
        decoration_group.update(screen_scroll)
        water_group.update(screen_scroll)
        exit_group.update(screen_scroll)

        item_box_group.draw(screen)
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        for enemy in enemy_group:
            enemy.update()
            enemy.draw()
            enemy.ai()
        player.update()
        player.draw()


world = World()
player, health_bar = world.process_data(load_level(LEVEL))


while run:
    clock.tick(FPS)

    if not start_game:
        if start_btn.draw(screen):
            start_game = True
        if exit_btn.draw(screen):
            run = False
    else:
        draw_bg()
        world.draw()
        if player.living:
            if shoot:
                player.shoot()
            elif throw and not grenade_thrown:
                throw_grenade()
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            if level_complete:
                LEVEL += 1
                if LEVEL < MAX_LEVELS:
                    screen_scroll = 0
                    bg_scroll = 0
                    world = World()
                    player, health_bar = world.process_data(load_level(LEVEL))
        else:
            screen_scroll = 0
            if restart_btn.draw(screen):
                bg_scroll = 0
                world = World()
                player, health_bar = world.process_data(load_level(LEVEL))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                shoot = True
            elif event.key == pygame.K_g:
                throw = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if player.living:
                    player.jump = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shoot = False
            elif event.key == pygame.K_g:
                throw = False
                grenade_thrown = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
    
    pygame.display.update()

pygame.quit()