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

    easy_button = Button(65, 500, 120, 50, BUTTON_COLOR, "EASY", BUTTON_TEXT_COLOR, 50)
    medium_button = Button(220, 500, 160, 50, BUTTON_COLOR, "MEDIUM", BUTTON_TEXT_COLOR, 50)
    hard_button = Button(420, 500, 120, 50, BUTTON_COLOR, "HARD", BUTTON_TEXT_COLOR, 50)
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

    return easy_button, medium_button, hard_button


def draw_game_in_progress(width, height, screen, difficulty):
    screen.fill(BOARD_COLOR)
    screen.fill(BG_COLOR, (0, CELL_SIZE * 9, WIDTH, 160))
    board = Board(width, (height - 100), screen, difficulty)
    board.draw()
    selected_row = 0
    selected_col = 0

    reset_button = Button(50, 620, 130, 60, BUTTON_COLOR, "RESET", BUTTON_TEXT_COLOR, 50)
    restart_button = Button(205, 620, 200, 60, BUTTON_COLOR, "RESTART", BUTTON_TEXT_COLOR, 50)
    exit_button = Button(430, 620, 110, 60, BUTTON_COLOR, "EXIT", BUTTON_TEXT_COLOR, 50)
    reset_button.draw(screen)
    restart_button.draw(screen)
    exit_button.draw(screen)

    # while the board is not full, keep looking for inputs
    while not board.is_full():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # mouse button inputs
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # sets value of click to board.click, value is None if not on board
                click = board.click(x, y)

                if reset_button.is_clicked(x, y):
                    board.reset_to_original()
                # BUGGED, FIX LATER
                if restart_button.is_clicked(x, y):
                    return "restart"
                if exit_button.is_clicked(x, y):
                    pygame.quit()
                    sys.exit()

                if click is not None:  # if click is on board
                    selected_row, selected_col = click  # sets the row and col to the row and column clicked on

            # key press inputs
            if event.type == pygame.KEYDOWN:
                # moves cells down, up, also makes sure it doesn't go out of bounds
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if selected_row < 8:
                        selected_row += 1
                    else:
                        selected_row = 8
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if selected_row > 0:
                        selected_row -= 1
                    else:
                        selected_row = 0
                # moves cells right, left, prevents out of bounds
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if selected_col < 8:
                        selected_col += 1
                    else:
                        selected_col = 8
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if selected_col > 0:
                        selected_col -= 1
                    else:
                        selected_col = 0

                # looks for number inputs, which will sketch the value
                # sorry it's a bit messy, it just checks for the number keys 1-9
                if ((event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or
                        event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or
                        event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9) and
                        board.original[selected_row][selected_col] == 0):
                    board.sketch(int(pygame.key.name(event.key)))

                # pressing enter key will "submit" the sketched value on that cell
                if event.key == pygame.K_RETURN and board.original[selected_row][selected_col] == 0:
                    board.place_number(board.selected.sketched_value)

                # clears the selected cell
                if event.key == pygame.K_BACKSPACE:
                    board.clear()

        # updates the board again
        board.select(selected_row, selected_col)
        screen.fill(BOARD_COLOR)
        screen.fill(BG_COLOR, (0, 600, WIDTH, 100))
        board.draw()
        reset_button.draw(screen)
        restart_button.draw(screen)
        exit_button.draw(screen)
        board.update_board()

        pygame.display.update()

    # returns True/False depending on if the board is correct
    return board.check_board()


def draw_game_over(winner):
    screen.fill(BG_COLOR)
    game_over_font = pygame.font.Font(None, GAME_OVER_FONT)
    option_font = pygame.font.Font(None, RESTART_FONT)

    if winner != 0:
        end_text = "Game Won!"
        exit_button = Button(240, 400, 110, 60, BUTTON_COLOR, "EXIT", BUTTON_TEXT_COLOR, 50)
        exit_button.draw(screen)
        end_surf = game_over_font.render(end_text, 0, TEXT_COLOR)
        end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        screen.blit(end_surf, end_rect)
        return exit_button
    else:
        end_text = "Game Over :("
        restart_button = Button(190, 400, 200, 60, BUTTON_COLOR, "RESTART", BUTTON_TEXT_COLOR, 50)
        restart_button.draw(screen)
        end_surf = game_over_font.render(end_text, 0, TEXT_COLOR)
        end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
        screen.blit(end_surf, end_rect)
        return restart_button


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
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if easy.is_clicked(x, y):
                        difficulty = 30
                    elif medium.is_clicked(x, y):
                        difficulty = 40
                    elif hard.is_clicked(x, y):
                        difficulty = 50

                if difficulty is not None:
                    win = draw_game_in_progress(WIDTH, HEIGHT, screen, difficulty)

                    if win == "restart":
                        difficulty = None
                        easy, medium, hard = draw_game_start()
                        pygame.display.update()

                    elif win:
                        game_over = True
                        winner = 1
                        pygame.display.update()
                        pygame.time.delay(1000)

                    elif not win:
                        winner = 0
                        game_over = True
                        pygame.time.delay(1000)


            if game_over:
                pygame.display.update()
                button = draw_game_over(winner)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button.is_clicked(x, y) and winner != 0:
                        pygame.quit()
                        sys.exit()
                    elif button.is_clicked(x, y):
                        difficulty = None
                        game_over = False
                        easy, medium, hard = draw_game_start()


        pygame.display.update()


if __name__ == "__main__":
    main()
