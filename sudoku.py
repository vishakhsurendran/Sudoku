import pygame  # imports pygame
import sys  # imports sys
from constants import *  # imports all constants from constants.py
from board import Board  # imports Board class from board.py
from sudoku_generator import *  # imports everything from sudoku_generator.py

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # initialize game window
pygame.display.set_caption("Sudoku")  # Sets game window caption to "Sudoku"
screen.fill(BG_COLOR)  # Fills screen with assigned background color (BG_COLOR)

''' 
Button class was adapted from a sample program in a Stack Overflow post by Patryk Karbowy.
https://stackoverflow.com/questions/63435298/how-to-create-a-button-class-in-pygame

The Button class' is_clicked() function makes use of a built-in function found in the Pygame documentation.
https://www.pygame.org/docs/ref/rect.html 

'''


class Button:  # Button class which creates and displays functioning buttons. Source cited above.
    def __init__(self, x, y, width, height, color, text, text_color, font_size):
        # initializes instance of Button object. Assigns passed in values as needed.
        self.rect = pygame.Rect(x, y, width, height)  # Creates button shape (rectangle)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)  # creates font for Button using passed-in size

    def draw(self, screen):  # method to draw Button to screen
        pygame.draw.rect(screen, self.color, self.rect)  # draws rectangle to screen using self.color and self.rect
        text_surf = self.font.render(self.text, True, self.text_color)  # creates surface for button text
        # (initializes button text and style)
        text_rect = text_surf.get_rect(center=self.rect.center)  # creates rect for text_surf
        # (assigns location for text on screen in Button)
        screen.blit(text_surf, text_rect)  # displays Button on screen using text_surf and text_rect

    def is_clicked(self, x, y):  # method to determine if Button on screen has been clicked by user
        return self.rect.collidepoint(x, y)  # returns True if passed in tuple (point) is located within
        # Button object's rectangle. If True, button has been clicked. Returns False if point is outside of rectangle
        # and button has not been clicked.


def draw_game_start():  # function to draw game-start screen
    screen.fill(BG_COLOR)  # Fills screen with assigned background color
    welcome_text = "Welcome to Sudoku"  # assigns welcome text to variable
    select = "Select Game Mode:"  # assigns selection text to variable
    welcome_font = pygame.font.Font(None, WELCOME_FONT)  # creates font for welcome_text using assigned font size
    select_font = pygame.font.Font(None, RESTART_FONT)  # creates font for selection text using assigned font size

    start_surf = welcome_font.render(welcome_text, 0, TEXT_COLOR)  # creates welcome_text surface
    # (generates text for display)
    start_rect = start_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))  # creates rect for start_surf
    # (assigns location for text on screen)
    screen.blit(start_surf, start_rect)  # displays welcome_text on screen using start_surf and start_rect

    select_surf = select_font.render(select, 0, TEXT_COLOR)  # creates selection text surface
    # (generates text for display)
    select_rect = select_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # creates rect for select_surf
    # (assigns location for text on screen)
    screen.blit(select_surf, select_rect)  # displays select_text on screen using select_surf and select_rect

    # creates three Button objects for three difficulty options
    easy_button = Button(65, 500, 120, 50, BUTTON_COLOR, "EASY", BUTTON_TEXT_COLOR, 50)
    medium_button = Button(220, 500, 160, 50, BUTTON_COLOR, "MEDIUM", BUTTON_TEXT_COLOR, 50)
    hard_button = Button(420, 500, 120, 50, BUTTON_COLOR, "HARD", BUTTON_TEXT_COLOR, 50)
    easy_button.draw(screen)  # draws easy difficulty button to screen
    medium_button.draw(screen)  # draws medium difficulty button to screen
    hard_button.draw(screen)  # draws hard difficulty button to screen

    # returns Button objects from start screen for interaction in main method
    return easy_button, medium_button, hard_button


def draw_game_in_progress(width, height, screen, difficulty):  # function to draw game in progress screen
    screen.fill(BOARD_COLOR)  # fills screen with assigned board color (light blue)
    screen.fill(BG_COLOR, (0, CELL_SIZE * 9, WIDTH, 160))  # fills bottom of screen with background color (white)
    board = Board(width, (height - 100), screen, difficulty)  # creates Board class object and assigns to board variable
    board.draw()  # calls draw() method on board to draw board to screen
    selected_row = 0  # creates selected_row variable and initializes to 0
    selected_col = 0  # creates selected_col variable and initializes to 0

    # creates reset, restart, and exit buttons as objects of Button class
    reset_button = Button(50, 620, 130, 60, BUTTON_COLOR, "RESET", BUTTON_TEXT_COLOR, 50)
    restart_button = Button(205, 620, 200, 60, BUTTON_COLOR, "RESTART", BUTTON_TEXT_COLOR, 50)
    exit_button = Button(430, 620, 110, 60, BUTTON_COLOR, "EXIT", BUTTON_TEXT_COLOR, 50)
    reset_button.draw(screen)  # draws reset_button to screen
    restart_button.draw(screen)  # draws restart_button to screen
    exit_button.draw(screen)  # draws exit_button to screen

    while not board.is_full():  # while the board is not full, continue looking for inputs
        for event in pygame.event.get():  # for each event
            if event.type == pygame.QUIT:  # if user clicks X button while in game in progress screen
                pygame.quit()  # quits pygame and closes window; program terminates
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # if user clicks mouse button
                x, y = event.pos  # assigns click location to x and y variables (tuple)
                # sets value of click to board.click, value is None if not on board
                click = board.click(x, y)  # calls click method on board using click location and assigns returned
                # value to click variable. Click is None if (x, y) is not on board.

                if reset_button.is_clicked(x, y):  # uses is_clicked method to check if reset_button has been clicked
                    board.reset_to_original()  # if reset_button is clicked, reset_to_original() method is called and
                    # board is reset to original condition.
                if restart_button.is_clicked(x, y):  # uses is_clicked() to check if restart_button has been clicked
                    return "restart"  # if restart_button is clicked, returns "restart" to reflect button click so
                    # necessary changes can be implemented in main function to return to game start screen.
                if exit_button.is_clicked(x, y):  # uses is_clicked method to check if exit_button has been clicked
                    pygame.quit()  # if exit_button is clicked, quits pygame and closes window; program terminates
                    sys.exit()

                if click is not None:  # if click is located on board
                    selected_row, selected_col = click  # sets the selected_row and selected_col to the row and column
                    # clicked on by user

            # key press inputs
            if event.type == pygame.KEYDOWN:  # executes if a key is pressed on the keyboard
                # moves cells down, up, also makes sure it doesn't go out of bounds
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # if pressed key is Down Arrow or "S"
                    if selected_row < 8:  # if selected_row is before last row (Checks bounds)
                        selected_row += 1  # increase selected_row to move selection down in board
                    else:  # if selected_row is not a row before last row
                        selected_row = 8  # selected_row is last row of board
                if event.key == pygame.K_UP or event.key == pygame.K_w:  # if pressed key is Up Arrow or "W"
                    if selected_row > 0:  # if selected_row is greater than 0 (Checks bounds)
                        selected_row -= 1  # decreases selected_row to move selection up in board
                    else:  # if selected_row is not a row after first row of board
                        selected_row = 0  # selected_row is first row of board
                # moves cells right, left, prevents out of bounds
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # if pressed key is Right Arrow or "D"
                    if selected_col < 8:  # if selected_col is before right-most column (Checks bounds)
                        selected_col += 1  # increase selected_col to move selection right in board
                    else:  # if selected_col is not before right-most column
                        selected_col = 8  # selected_col is right-most column in board
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # if pressed key is Left Arrow or "A"
                    if selected_col > 0:  # if selected_col is beyond left-most column (Checks bounds)
                        selected_col -= 1  # decreases selected_col to move selection left in board
                    else:  # if selected_col is not beyond left-most column
                        selected_col = 0  # selected_col is left-most column in board

                # checks if number keys 1-9 have been pressed and cell was not randomly generated
                if ((event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or
                        event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or
                        event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9) and
                        board.original[selected_row][selected_col] == 0):
                    board.sketch(int(pygame.key.name(event.key)))  # if true, pressed keys' value is sketched to
                    # selected cell

                # places sketched number in selected cell if enter key is pressed and cell was not randomly generated
                if event.key == pygame.K_RETURN and board.original[selected_row][selected_col] == 0:
                    board.place_number(board.selected.sketched_value)  # selected sketch value is placed into cell

                # clears the selected cell if backspace key is pressed and cell was not randomly generated
                if event.key == pygame.K_BACKSPACE and board.original[selected_row][selected_col] == 0:
                    board.clear()  # uses clear() method to empty selected cell.

        # updates the board again
        board.select(selected_row, selected_col)
        screen.fill(BOARD_COLOR)  # fills screen with assigned board color (light blue)
        screen.fill(BG_COLOR, (0, 600, WIDTH, 100))  # fills bottom of screen behind buttons with background color
        board.draw()  # calls draw() method on board to draw board to screen
        reset_button.draw(screen)  # draws reset_button on screen again
        restart_button.draw(screen)  # draws restart_button on screen again
        exit_button.draw(screen)  # draws exit_button on screen again
        board.update_board()  # updates board using update_board() with new values

        pygame.display.update()  # display is updated after event

    return board.check_board()  # returns True or False depending on if board matches solution


def draw_game_over(winner):  # function to display game over screen
    screen.fill(BG_COLOR)  # Fills screen with background color
    game_over_font = pygame.font.Font(None, GAME_OVER_FONT)  # initialize font for game over message
    # using assigned font size

    if winner != 0:  # if winner variable is not 0, game is won
        end_text = "Game Won!"  # end_text variable is assigned game won text
        # creates exit Button object for use on game over screen when game is won
        exit_button = Button(240, 400, 110, 60, BUTTON_COLOR, "EXIT", BUTTON_TEXT_COLOR, 50)
        exit_button.draw(screen)  # draws exit button to screen
        end_surf = game_over_font.render(end_text, 0, TEXT_COLOR)  # creates end_text surface
        # (generates text to display)
        end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))  # creates rect for end_surf
        # (assigns location for text on screen)
        screen.blit(end_surf, end_rect)  # displays end_text to screen using end_surf and end_rect
        return exit_button  # returns exit Button object for interaction in main method
    else:  # if winner variable is 0, game over (lost)
        end_text = "Game Over :("  # end_text variable is assigned game over text
        # creates restart Button object for use on game over screen when game is lost
        restart_button = Button(190, 400, 200, 60, BUTTON_COLOR, "RESTART", BUTTON_TEXT_COLOR, 50)
        restart_button.draw(screen)  # draws restart button to screen
        end_surf = game_over_font.render(end_text, 0, TEXT_COLOR)  # creates end_text surface
        # (generates text to display)
        end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))  # creates rect for end_surf
        # (assigns location for text on screen)
        screen.blit(end_surf, end_rect)  # displays end_text to screen using end_surf and end_rect
        return restart_button  # returns restart Button object for interaction in main method


def main():  # main function

    winner = 0  # initializes winner variable to 0
    game_over = False  # initializes game_over variable to False
    difficulty = None  # initializes difficulty variable to None

    easy, medium, hard = draw_game_start()  # calls draw_game_start() function and
    # assigns returned values to appropriate variables

    while True:  # event loop
        for event in pygame.event.get():  # for each event
            if event.type == pygame.QUIT:  # if user clicks X button
                pygame.quit()  # quits pygame and closes window; program terminates
                sys.exit()
            if not game_over:  # if game_over is False
                if event.type == pygame.MOUSEBUTTONDOWN:  # if user clicks mouse button
                    x, y = event.pos  # assigns click location to x and y variables
                    if easy.is_clicked(x, y):  # if easy difficulty button is clicked
                        difficulty = 30  # difficulty is set to 30. 30 blank spaces in Sudoku grid
                    elif medium.is_clicked(x, y):  # if medium difficulty button is clicked
                        difficulty = 40  # difficulty is set to 40. 40 blank spaces in Sudoku grid
                    elif hard.is_clicked(x, y):  # if hard difficulty button is clicked
                        difficulty = 50  # difficulty is set to 50. 50 blank spaces in Sudoku grid

                if difficulty is not None:  # Once difficulty has been selected by user
                    win = draw_game_in_progress(WIDTH, HEIGHT, screen, difficulty)  # draw_game_in_progress is called
                    # and assigns returned True/False value to win variable based on whether board matches solution

                    if win == "restart":  # If "restart" is returned from draw_game_in_progress() function
                        difficulty = None  # difficulty is set to None again
                        easy, medium, hard = draw_game_start()  # draw_game_start() is called to display start screen
                        pygame.display.update()  # display is updated

                    elif win:  # If win is True
                        game_over = True  # game_over is set to True
                        winner = 1  # winner variable is updated to 1 to indicate game has been won
                        pygame.display.update()  # display is updated to show player's last move
                        pygame.time.delay(1000)  # time delay by 1 second to show player's last move on screen

                    elif not win:  # If win is False
                        winner = 0  # winner variable remains 0 to indicate game has not been won
                        game_over = True  # game_over is set to True to indicate game is over
                        pygame.time.delay(1000)  # time delay by 1 second to show player's last move on screen

            if game_over:  # If game_over has been set to True
                pygame.display.update()  # display is updated
                button = draw_game_over(winner)  # draw_game_over() function is called and winner variable is passed in.
                # returned Button object is assigned to button variable.
                if event.type == pygame.MOUSEBUTTONDOWN:  # If user clicks mouse button
                    x, y = event.pos  # assigns click location to x and y variables
                    if button.is_clicked(x, y) and winner != 0:  # checks if button has been clicked at event location
                        # and checks if winner is no longer 0
                        pygame.quit()  # quits pygame and closes window; program terminates
                        sys.exit()
                    elif button.is_clicked(x, y):  # if winner is 0 and button is clicked
                        difficulty = None  # difficulty is set to None again
                        game_over = False  # game_over is set to False again
                        easy, medium, hard = draw_game_start()  # calls draw_game_start() function again and
                        # displays start screen again

        pygame.display.update()  # display is updated after event


if __name__ == "__main__":  # calls main function and executes program
    main()
