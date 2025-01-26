import pygame
from pygame.locals import *
import random as r

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([100, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > WIDTH - 100:
            self.rect.x = WIDTH - 100
        elif self.rect.x < 0:
            self.rect.x = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Инициализация скорости шарика
        self.vx = 0
        self.vy = 0

    def start_movement(self):
        self.vx = r.choice([-1, 1])  # Случайное направление
        self.vy = 1  # Начальная скорость вниз


    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top <= 0:
            self.vy = -self.vy
        if self.rect.right >= WIDTH:
            self.vx = -self.vx
        if self.rect.left <= 0:
            self.vx = -self.vx
        if self.rect.colliderect(platform.rect) and self.vy > 0:
            self.vy = -self.vy
            self.rect.bottom = platform.rect.top


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def show_start_screen():
    screen.fill(BLACK)
    title_font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 48)
    draw_text('Игра Арканоид', title_font, GREEN, screen, 250, 200)
    pygame.draw.rect(screen, WHITE, (300, 300, 200, 100))
    draw_text('Start', button_font, GREEN, screen, 360, 335)
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                start = False
        pygame.display.flip()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, all_sprites):
        super().__init__(all_sprites)
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


platform = Platform(WIDTH // 2, HEIGHT - 50)
ball = Ball(WIDTH // 2, HEIGHT - 50)

all_sprites = pygame.sprite.Group()
borders = pygame.sprite.Group()

left_border = Border(0, 0, 0, HEIGHT, borders)
right_border = Border(WIDTH, 0, WIDTH, HEIGHT, borders)
top_border = Border(0, 0, WIDTH, 0, borders)

all_sprites.add(platform)
all_sprites.add(ball)
all_sprites.add(left_border)
all_sprites.add(right_border)
all_sprites.add(top_border)

show_start_screen()

# Запуск движения мяча будет происходить только после нажатия на кнопку
ball.start_movement()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()