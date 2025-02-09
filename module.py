import pygame
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
