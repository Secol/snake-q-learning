import pygame
import random
import numpy as np

class Snake:
    def __init__(self, display_width, display_height, snake_block):
        self.snake_block = snake_block
        self.display_width = display_width
        self.display_height = display_height
        self.direction = 'RIGHT'
        self.reset()

    def reset(self):
        self.x = self.display_width // 2
        self.y = self.display_height // 2
        self.x_change = self.snake_block
        self.y_change = 0
        self.snake_List = []
        self.length_of_snake = 1

    def update_position(self):
        self.x += self.x_change
        self.y += self.y_change

    def check_collision(self):
        if self.x >= self.display_width or self.x < 0 or self.y >= self.display_height or self.y < 0:
            return True
        for segment in self.snake_List[:-1]:
            if segment == [self.x, self.y]:
                return True
        return False

    def grow(self):
        self.length_of_snake += 1

    def move(self):
        snake_head = [self.x, self.y]
        self.snake_List.append(snake_head)
        if len(self.snake_List) > self.length_of_snake:
            del self.snake_List[0]

    def set_direction(self, direction):
        if direction == 'LEFT' and self.direction != 'RIGHT':
            self.x_change = -self.snake_block
            self.y_change = 0
            self.direction = 'LEFT'
        elif direction == 'RIGHT' and self.direction != 'LEFT':
            self.x_change = self.snake_block
            self.y_change = 0
            self.direction = 'RIGHT'
        elif direction == 'UP' and self.direction != 'DOWN':
            self.y_change = -self.snake_block
            self.x_change = 0
            self.direction = 'UP'
        elif direction == 'DOWN' and self.direction != 'UP':
            self.y_change = self.snake_block
            self.x_change = 0
            self.direction = 'DOWN'

class SnakeGame:
    def __init__(self, display_width=600, display_height=400, border=30, snake_block=10, snake_speed=20):
        pygame.init()
        self.display_width = display_width
        self.display_height = display_height
        self.border = border
        self.game_width = display_width - 2 * border
        self.game_height = display_height - 2 * border
        self.snake_block = snake_block
        self.snake_speed = snake_speed
        self.display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('Jogo da Cobrinha Para Iniciantes em q-Learning')
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.display_width, self.display_height, self.snake_block)
        self.foodx = None
        self.foody = None
        self.reset()

    def reset(self):
        self.snake.reset()
        self.foodx = round(random.randrange(self.border, self.display_width - self.border - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(self.border, self.display_height - self.border - self.snake_block) / 10.0) * 10.0

    def game_score(self, score):
        font = pygame.font.SysFont("consolas", 24)
        value = font.render(f"Pontuação > {score}", True, white)
        self.display.blit(value, [self.display_width // 2 - value.get_width() // 2, self.border // 2 - value.get_height() // 2])

    def draw_snake(self):
        for segment in self.snake.snake_List:
            pygame.draw.rect(self.display, red, [segment[0], segment[1], self.snake_block, self.snake_block])

    def game_over_message(self, score):
        font = pygame.font.SysFont("consolas", 50)
        message = font.render("GAME OVER!", True, red)
        score_message = font.render(f"Pontuação: {score}", True, red)
        self.display.blit(message, [self.display_width // 2 - message.get_width() // 2, self.display_height // 2 - message.get_height()])
        self.display.blit(score_message, [self.display_width // 2 - score_message.get_width() // 2, self.display_height // 2])

    def draw_borders_and_guides(self):
        pygame.draw.rect(self.display, grey, [0, 0, self.display_width, self.border])  # Topo
        pygame.draw.rect(self.display, grey, [0, 0, self.border, self.display_height])  # Esquerda
        pygame.draw.rect(self.display, grey, [0, self.display_height - self.border, self.display_width, self.border])  # Fundo
        pygame.draw.rect(self.display, grey, [self.display_width - self.border, 0, self.border, self.display_height])  # Direita

        for i in range(self.border, self.display_width - self.border, self.snake_block):
            pygame.draw.line(self.display, grey, (i, self.border), (i, self.display_height - self.border), 1)
        for i in range(self.border, self.display_height - self.border, self.snake_block):
            pygame.draw.line(self.display, grey, (self.border, i), (self.display_width - self.border, i), 1)

    def update_food_position(self):
        self.foodx = round(random.randrange(self.border, self.display_width - self.border - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(self.border, self.display_height - self.border - self.snake_block) / 10.0) * 10.0

    def run(self):
        game_over = False
        game_close = False

        while not game_over:
            while game_close:
                self.display.fill(black)
                self.game_over_message(self.snake.length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.reset()
                            game_close = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.set_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction('RIGHT')
                    elif event.key == pygame.K_UP:
                        self.snake.set_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction('DOWN')

            self.snake.update_position()

            if self.snake.check_collision():
                game_close = True

            self.display.fill(black)
            self.draw_borders_and_guides()
            pygame.draw.rect(self.display, green, [self.foodx, self.foody, self.snake_block, self.snake_block])
            self.snake.move()
            self.draw_snake()
            self.game_score(self.snake.length_of_snake - 1)

            pygame.display.update()

            if self.snake.x == self.foodx and self.snake.y == self.foody:
                self.update_food_position()
                self.snake.grow()

            self.clock.tick(self.snake_speed)

        pygame.quit()

if __name__ == "__main__":
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    grey = (100, 100, 100)

    game = SnakeGame()
    game.run()