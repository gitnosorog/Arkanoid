import pygame
from pygame.locals import *
import random as r

pygame.init()

WIDTH = 800
HEIGHT = 600


class Arkanoid():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Arkanoid')

        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        self.platform = self.Platform(WIDTH // 2, HEIGHT - 50, self)
        self.ball = self.Ball(WIDTH // 2, HEIGHT - 50, self)

        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        left_border = self.Border(0, 0, 0, HEIGHT, self.borders)
        right_border = self.Border(WIDTH, 0, WIDTH, HEIGHT, self.borders)
        top_border = self.Border(0, 0, WIDTH, 0, self.borders)

        self.all_sprites.add(self.platform)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(left_border)
        self.all_sprites.add(right_border)
        self.all_sprites.add(top_border)

        self.create_blocks()

    def create_blocks(self):
        colors = [self.RED, self.GREEN, self.BLUE, self.YELLOW]
        block_width = 75
        block_height = 30
        for row in range(5):
            for col in range(10):
                color = r.choice(colors)
                x = col * (block_width + 10) + 35
                y = row * (block_height + 10) + 50
                block = self.Block(x, y, color, self.blocks)
                self.all_sprites.add(block)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def show_start_screen(self):
        self.screen.fill(self.BLACK)
        title_font = pygame.font.SysFont(None, 72)
        button_font = pygame.font.SysFont(None, 48)
        self.draw_text('Игра Арканоид', title_font, self.GREEN, self.screen, 250, 200)
        pygame.draw.rect(self.screen, self.WHITE, (300, 300, 200, 100))
        self.draw_text('Start', button_font, self.GREEN, self.screen, 360, 335)
        start = True
        while start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    start = False
            pygame.display.flip()

    def run(self):
        self.show_start_screen()
        self.ball.start_movement()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.all_sprites.update()

            hits = pygame.sprite.spritecollide(self.ball, self.blocks, True)
            for hit in hits:
                self.ball.vy = -self.ball.vy

            self.screen.fill(self.BLACK)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, game):
            super().__init__()
            self.image = pygame.Surface([100, 20])
            self.image.fill(game.WHITE)
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
        def __init__(self, x, y, game):
            super().__init__()
            self.image = pygame.Surface((15, 15))
            self.image.fill(game.RED)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.vx = 0
            self.vy = 0
            self.platform = game.platform

        def start_movement(self):
            self.vx = r.choice([-1, 1])
            self.vy = 1

        def update(self):
            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.top <= 0:
                self.vy = -self.vy
            if self.rect.right >= WIDTH:
                self.vx = -self.vx
            if self.rect.left <= 0:
                self.vx = -self.vx

            if self.rect.colliderect(self.platform.rect) and self.vy > 0:
                self.vy = -self.vy
                self.rect.bottom = self.platform.rect.top

    class Block(pygame.sprite.Sprite):
        def __init__(self, x, y, color, all_sprites):
            super().__init__(all_sprites)
            self.image = pygame.Surface((75, 30))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Border(pygame.sprite.Sprite):
        def __init__(self, x1, y1, x2, y2, all_sprites):
            super().__init__(all_sprites)
            if x1 == x2:
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == '__main__':
    game = Arkanoid()
    game.run()