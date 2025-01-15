import pygame
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# Класс платформы
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


# Класс шарика
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 1
        self.speed_y = -1

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Проверяем границы экрана
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1

        # Проверяем столкновение с платформой
        if self.rect.colliderect(platform.rect):
            self.speed_y *= -1


# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Функция для отображения начального экрана
def show_start_screen():
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                start = False

        screen.fill(BLACK)
        title_font = pygame.font.SysFont(None, 72)
        button_font = pygame.font.SysFont(None, 48)
        draw_text('Игра Арканоид', title_font, GREEN, screen, 250, 200)
        pygame.draw.rect(screen, WHITE, (300, 300, 200, 100))
        draw_text('Start', button_font, GREEN, screen, 360, 335)
        pygame.display.flip()


# Создание платформы
platform = Platform(WIDTH // 2, HEIGHT - 50)

# Создание шарика
ball = Ball(WIDTH // 2, HEIGHT - 150)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(platform)
all_sprites.add(ball)

# Показываем начальный экран
show_start_screen()

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Обновление всех спрайтов
    all_sprites.update()

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование всех спрайтов
    all_sprites.draw(screen)

    # Обновление дисплея
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
