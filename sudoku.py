import pygame, sys
from constants import *
from board import Board
from sudoku_generator import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
screen.fill(BG_COLOR)


class Button:
    def __init__(self, x, y, width, height, color, text, text_color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, x, y):
        return self.rect.collidepoint(x, y)


def draw_game_start():
    screen.fill(BG_COLOR)
    welcome_text = "Welcome to Sudoku"
    select = "Select Game Mode:"
    welcome_font = pygame.font.Font(None, WELCOME_FONT)
    select_font = pygame.font.Font(None, RESTART_FONT)
    options_font = pygame.font.Font(None, OPTIONS_FONT)

    start_surf = welcome_font.render(welcome_text, 0, TEXT_COLOR)
    start_rect = start_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    screen.blit(start_surf, start_rect)

    select_surf = select_font.render(select, 0, TEXT_COLOR)
    select_rect = select_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(select_surf, select_rect)

    easy_button = Button(65, 500, 120, 50, BUTTON_COLOR, "EASY", TEXT_COLOR, 50)
    medium_button = Button(220, 500, 160, 50, BUTTON_COLOR, "MEDIUM", TEXT_COLOR, 50)
    hard_button = Button(420, 500, 120, 50, BUTTON_COLOR, "HARD", TEXT_COLOR, 50)
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

    return easy_button, medium_button, hard_button


def draw_game_in_progress(width, height, screen, difficulty):
    screen.fill(BG_COLOR)
    board = Board(width, (height - 100), screen, difficulty)
    board.draw()

    reset_button = Button(80, 50, 130, 50, BUTTON_COLOR, "RESET", TEXT_COLOR, 50)
    restart_button = Button(200, 50, 130, 50, BUTTON_COLOR, "RESTART", TEXT_COLOR, 50)
    exit_button = Button(550, 50, 130, 50, BUTTON_COLOR, "EXIT", TEXT_COLOR, 50)
    reset_button.draw(screen)
    restart_button.draw(screen)
    exit_button.draw(screen)


def draw_game_over(winner):
    screen.fill(BG_COLOR)
    game_over_font = pygame.font.Font(None, GAME_OVER_FONT)
    option_font = pygame.font.Font(None, RESTART_FONT)
    if winner != 0:
        end_text = "Game Won!"
    else:
        end_text = "Game Over :("

    end_surf = game_over_font.render(end_text, 0, TEXT_COLOR)
    end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    screen.blit(end_surf, end_rect)

    restart_text = "Restart"
    restart_surf = option_font.render(restart_text, 0, TEXT_COLOR)
    restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(restart_surf, restart_rect)


def main():

    player = 1
    winner = 0
    game_start = False
    game_over = False
    difficulty = None

    easy, medium, hard = draw_game_start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                while difficulty is None:
                    if easy.is_clicked(x, y):
                        difficulty = 30
                    elif medium.is_clicked(x, y):
                        difficulty = 40
                    elif hard.is_clicked(x, y):
                        difficulty = 50

                draw_game_in_progress(WIDTH, HEIGHT, screen, difficulty)
                pygame.display.update()

        if game_over:
            pygame.display.update()
            pygame.time.delay(1000)
            draw_game_over(winner)
        # for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # x, y = event.pos
            # if x <=

        pygame.display.update()


if __name__ == "__main__":
    main()
