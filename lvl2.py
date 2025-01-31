import pygame
from pygame.locals import *
import random
from pygame.sprite import Sprite

WIDTH = 800
HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Класс платформы
class Platform(Sprite):
    def __init__(self, x, y, width=100, height=20, color=WHITE):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = max(min(pos[0], WIDTH - self.rect.width), 0)


# Класс мяча
class Ball(Sprite):
    def __init__(self, x, y, radius=7.5, color=RED):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(BG_COLOR)
        self.image.set_colorkey(BG_COLOR)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = 0
        self.vy = 0
        self.platform = None

    def start_movement(self):
        self.vx = random.choice([-1, 1]) * 5
        self.vy = -5

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top <= 0:
            self.vy *= -1
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.vx *= -1

        if self.platform and self.rect.colliderect(self.platform.rect) and self.vy > 0:
            self.vy *= -1
            self.rect.bottom = self.platform.rect.top


# Класс блока
class Block(Sprite):
    def __init__(self, x, y, width=75, height=30, color=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color or RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс границы
class Border(Sprite):
    def __init__(self, x1, y1, x2, y2, color=WHITE):
        super().__init__()
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill(color)


# Класс уровня
class Level:
    def __init__(self):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        self.platform = Platform(WIDTH // 2, HEIGHT - 50)
        self.ball = Ball(WIDTH // 2, HEIGHT - 50)
        self.ball.platform = self.platform

        self.all_sprites.add(self.platform)
        self.all_sprites.add(self.ball)

        left_border = Border(0, 0, 0, HEIGHT)
        right_border = Border(WIDTH, 0, WIDTH, HEIGHT)
        top_border = Border(0, 0, WIDTH, 0)

        self.all_sprites.add(left_border)
        self.all_sprites.add(right_border)
        self.all_sprites.add(top_border)

        self.create_blocks()

    def create_blocks(self):
        colors = [RED, GREEN, BLUE, YELLOW]
        block_width = 75
        block_height = 30
        offset_x = 30
        offset_y = 50
        num_rows = 9

        for row in range(num_rows):
            for col in range(num_rows - row):
                x = offset_x + col * (block_width + 10) + row * (block_width / 2 + 5)
                y = offset_y + row * (block_height + 10)
                block = Block(x, y, color=random.choice(colors))
                self.blocks.add(block)
                self.all_sprites.add(block)

    def check_victory(self):
        if len(self.blocks) == 0:
            self.win_screen()

    def win_screen(self):
        self.screen.fill(BG_COLOR)
        win_font = pygame.font.SysFont(None, 72)
        self.draw_text('Вы выиграли!', win_font, GREEN, 230, 220)
        next_level_font = pygame.font.SysFont(None, 36)
        self.draw_text('Нажмите любую клавишу для продолжения', next_level_font, WHITE, 180, 320)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    waiting = False

    def is_over(self):
        if self.ball.rect.y >= 600:
            self.game_over_screen()

    def game_over_screen(self):
        self.screen.fill(BG_COLOR)
        game_over_font = pygame.font.SysFont(None, 72)
        self.draw_text('Game Over', game_over_font, GREEN, 280, 240)
        pygame.display.flip()
        pygame.time.delay(2000)  # Пауза на 2 секунды
        self.show_start_screen()  # Возвращаемся к началу

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    def show_start_screen(self):
        self.screen.fill(BG_COLOR)
        title_font = pygame.font.SysFont(None, 72)
        button_font = pygame.font.SysFont(None, 48)
        self.draw_text('Игра Арканоид', title_font, GREEN, 250, 200)
        pygame.draw.rect(self.screen, WHITE, (300, 300, 200, 100))
        self.draw_text('Start', button_font, GREEN, 360, 335)
        start = True
        while start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    self.reset_game()
                    self.ball.start_movement()  # движение шарика после нажатия
                    start = False
            pygame.display.flip()

    def reset_game(self):
        self.__init__()

    def run(self):
        self.show_start_screen()

        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.all_sprites.update()
            self.is_over()  # Проверка проигрыша

            hits = pygame.sprite.spritecollide(self.ball, self.blocks, True)
            if hits:
                self.ball.vy = -self.ball.vy

            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.screen)
            if len(self.blocks) == 0:
                self.check_victory()
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    level = Level()
    level.run()