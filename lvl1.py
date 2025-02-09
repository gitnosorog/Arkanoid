import pygame
from pygame.locals import *
import random
import module as m
from lvl2 import Level2


# Класс уровня
class Level1:
    def __init__(self):
        self.screen = m.screen
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        self.platform = m.Platform(m.WIDTH // 2, m.HEIGHT - 50)
        self.ball = m.Ball(m.WIDTH // 2, m.HEIGHT - 50)
        self.ball.platform = self.platform

        self.all_sprites.add(self.platform)
        self.all_sprites.add(self.ball)

        left_border = m.Border(0, 0, 0, m.HEIGHT)
        right_border = m.Border(m.WIDTH, 0, m.WIDTH, m.HEIGHT)
        top_border = m.Border(0, 0, m.WIDTH, 0)

        self.all_sprites.add(left_border)
        self.all_sprites.add(right_border)
        self.all_sprites.add(top_border)

        self.create_blocks()

    def create_blocks(self):
        colors = [m.RED, m.GREEN, m.BLUE, m.YELLOW]
        block_width = 75
        block_height = 30

        # Основная стена
        for row in range(7):
            for col in range(3, 6):
                x = col * (block_width + 10) + 15
                y = row * (block_height + 10) + 50
                block = m.Block(x, y, color=random.choice(colors))
                self.blocks.add(block)
                self.all_sprites.add(block)


        # Левая башня
        for row in range(5):
            for col in range(2):
                x = col * (block_width + 10) + 15
                y = row * (block_height + 10) + 50
                block = m.Block(x, y, color=random.choice(colors))
                self.blocks.add(block)
                self.all_sprites.add(block)

        # Правая башня
        for row in range(5):
            for col in range(2):
                x = (col + 6) * (block_width + 10) + 95
                y = row * (block_height + 10) + 50
                block = m.Block(x, y, color=random.choice(colors))
                self.blocks.add(block)
                self.all_sprites.add(block)

    def win_screen(self):
        self.screen.fill(m.BG_COLOR)
        win_font = pygame.font.SysFont(None, 36)
        self.draw_text('Вы прошли!', win_font, m.GREEN, 230, 220)
        next_level_font = pygame.font.SysFont(None, 36)
        self.draw_text('Нажмите Enter чтобы пройти на следующий уровень', next_level_font, m.WHITE, 150, 320)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN or event.type == K_RETURN:
                    Level2().run()

    def is_over(self):
        if self.ball.rect.y >= 600:
            self.game_over_screen()

    def game_over_screen(self):
        self.screen.fill(m.BG_COLOR)
        game_over_font = pygame.font.SysFont(None, 72)
        self.draw_text('Game Over', game_over_font, m.GREEN, 280, 240)
        pygame.display.flip()
        pygame.time.delay(2000)  # Пауза на 2 секунды
        self.show_start_screen()  # Возвращаемся к началу

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    def show_start_screen(self):
        self.screen.fill(m.BG_COLOR)
        title_font = pygame.font.SysFont(None, 72)
        text_font = pygame.font.SysFont(None, 36)
        button_font = pygame.font.SysFont(None, 48)
        self.draw_text('Игра Арканоид', title_font, m.GREEN, 250, 150)
        self.draw_text('Башня. Уровень 1', text_font, m.WHITE, 270, 250)
        pygame.draw.rect(self.screen, m.WHITE, (300, 300, 200, 100))
        self.draw_text('Start', button_font, m.GREEN, 360, 335)
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

        IS_WIN = True
        running = True
        while running:
            m.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    quit()

            self.all_sprites.update()
            self.is_over()  # Проверка проигрыша

            hits = pygame.sprite.spritecollide(self.ball, self.blocks, True)
            if hits:
                self.ball.vy = -self.ball.vy

            self.screen.fill(m.BG_COLOR)
            self.all_sprites.draw(self.screen)
            if IS_WIN:
                if len(self.blocks) == 0:
                    self.win_screen()
                    IS_WIN = False

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    level = Level1()
    level.run()
