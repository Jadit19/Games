import pygame
from pygame.locals import *
import time
from config import isWallAnEnd, display_size, fill_color, speed, square_size
from src.Food import Food
from src.Snake import Snake

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.surface = pygame.display.set_mode((display_size[0]*square_size, display_size[1]*square_size))
        self.surface.fill(fill_color)
        
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.food = Food(self.surface)
        self.food.draw()

    def is_collission(self, x1, y1, x2, y2):
        if x1>=x2 and x1<x2+square_size:
            if y1>=y2 and y1<y2+square_size:
                return True
        return False

    def check_pos(self):
        flag = False
        for i in range(0, self.snake.length):
            if self.is_collission(self.food.x, self.food.y, self.snake.x[i], self.snake.y[i]):
                flag = True
        if flag:
            self.food.move()
            self.check_pos()

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255,0,0))
        self.surface.blit(score, (display_size[0]*square_size-130, 10))

    def show_game_over(self):
        self.surface.fill(fill_color)
        font = pygame.font.SysFont("arial", 30)
        line_1 = font.render(f"Score: {self.snake.length - 1}", True, (255, 0, 0))
        line_2 = font.render("To play again, press Enter. To exit, press Escape.", True, (255, 0, 0))
        self.surface.blit(line_1, (display_size[0]*square_size/2 - 50, display_size[1]*square_size/2 - 20))
        self.surface.blit(line_2, (display_size[0]*square_size/2 - 250, display_size[1]*square_size/2 + 20))
        pygame.display.flip()

    def reset_game(self):
        self.snake = Snake(self.surface, 1)
        self.food = Food(self.surface)

    def play(self):
        self.snake.move_snake()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        #! Snake colliding with food
        if self.is_collission(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.move()
            self.snake.increase_length()
            self.check_pos()
            # print("Food Eaten!")

        #! Snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collission(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over!"

        #! Snake colliding with boundary
        if isWallAnEnd:
            if self.is_collission(self.snake.x[0], self.snake.y[0], -square_size, self.snake.y[0]) or self.is_collission(self.snake.x[0], self.snake.y[0], display_size[0]*square_size, self.snake.y[0]) or self.is_collission(self.snake.x[0], self.snake.y[0], self.snake.x[0], -square_size) or self.is_collission(self.snake.x[0], self.snake.y[0], self.snake.x[0], display_size[1]*square_size):
                raise "Game Over!"

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key==K_LEFT or event.key==K_a:
                            self.snake.move_left()
                        elif event.key==K_RIGHT or event.key==K_d:
                            self.snake.move_right()
                        elif event.key==K_UP or event.key==K_w:
                            self.snake.move_up()
                        elif event.key==K_DOWN or event.key==K_s:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset_game()

            time.sleep(0.1/speed)

if __name__ == "__main__":
    game = Game()
    game.run()