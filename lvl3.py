import pygame
from pygame.locals import *
import random as r
import module as m

# Класс уровня
class Level3:
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
        for row in range(4):
            for col in range(10):
                color = r.choice(colors)
                x = col * (block_width + 10) + 35
                y = row * (block_height + 10) + 50
                block = m.Block(x, y, color=color)
                self.blocks.add(block)
                self.all_sprites.add(block)

    def win_screen(self):
        self.screen.fill(m.BG_COLOR)
        win_font = pygame.font.SysFont(None, 72)
        self.draw_text('Вы выиграли!', win_font, m.GREEN, 200, 220)
        next_level_font = pygame.font.SysFont(None, 36)
        self.draw_text('Поздравляю с победой, ты прошел в долину славы!', next_level_font, m.WHITE, 180, 320)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    waiting = False

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
        button_font = pygame.font.SysFont(None, 48)
        text_font = pygame.font.SysFont(None, 36)
        self.draw_text('Игра Арканоид', title_font, m.GREEN, 250, 150)
        self.draw_text('Блокада. Финал', text_font, m.WHITE, 270, 250)
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
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    level = Level3()
    level.run()

