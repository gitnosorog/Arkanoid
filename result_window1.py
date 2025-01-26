import pygame
from pygame.locals import *
from start_window_1lvl import Arkanoid

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Функция для отрисовки текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Функция для окна проигрыша
def fail_window():
    screen.fill(BLACK)
    title_font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 48)
    draw_text('К сожалению, Вы проиграли, попробуете еще раз?', pygame.font.SysFont('arial', 24), GREEN, screen, 100, 200)
    pygame.draw.rect(screen, WHITE, (300, 300, 200, 100))
    draw_text('Начать', button_font, GREEN, screen, 350, 335)
    pygame.display.flip()

    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 300 <= mouse_y <= 400:
                    start = False
                    Arkanoid().run()

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if not game_over:

        if True:
            game_over = True
    fail_window()

    screen.fill(BLACK)
    pygame.display.flip()

pygame.quit()