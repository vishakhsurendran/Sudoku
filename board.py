import pygame
from constants import *
from sudoku_generator import SudokuGenerator
from cell import Cell


class Board:
    # This is Samuel. I'll add my comments later
    def __init__(self, width, height, screen, difficulty): # Samuel A.
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = []
        self.correct_answer = SudokuGenerator.generate_sudoku()
        for row in range(9):
            arr = []
            for col in range(9):
                cell = Cell((0, row, col, screen))
                arr.append(cell)
            self.cells.append(arr)
        self.selected = None

    def draw(self): # Samuel A.
        # Sudoku grid lines
        for col in range(9):
            pygame.draw.line(self.screen, COLOR, [(col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT)], 4)
        for row in range(9):
            pygame.draw.line(self.screen, COLOR, [(0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE)], 4)

        # Bolded sudoku grid lines representing boxes
        for col in range(1, 4):
            pygame.draw.lines(self.screen, COLOR, False, [(col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT)], 1)
        for row in range(1, 4):
            pygame.draw.lines(self.screen, COLOR, False, [(0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE)], 1)

        # Draws cells
        for col in range(9):
            for row in range(9):
                self.cells[row][col].draw()

    def select(self, row, col):  # Vishakh S.
        self.selected = self.cells[row][col]  # selects new cell using row and col values

    def click(self, x, y): # Samuel A.
        # Finds row and col values from (x, y) coordinates
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < 9 and 0 <= col < 9:
            return row, col
        else:
            return None
            
    def clear(self): # Samuel A.
        # Clears selected and sketched values
        if self.selected:
            self.selected.set_cell_value(0)
            self.selected.set_sketched_value(0)

    def sketch(self, value): # Samuel A.
        # Sets sketched value to user entered sketch value
        if self.selected:
            self.selected.set_sketched_value(value)

    def place_number(self, value): # Samuel A.
        # Sets value to user entered value
        if self.selected:
            self.selected.set_cell_value(value)

    def reset_to_original(self):  # Vishakh S.
        for row in range(9):  # iterates through rows in Sudoku board
            for col in range(9):  # iterates through cols in Sudoku board
                cell = self.cells[row][col]  # assigns current value to cell variable
                original = self.board[row][col]  # gets original value from original board

                if original != 0:  # checks if original value is not 0
                    cell.set_cell_value(original)  # sets to corresponding digit
                else:  # if original value is 0
                    cell.set_cell_value(0)  # sets cell values to 0
                    cell.set_sketched_value(0)

    def is_full(self):  # Vishakh S.
        for row in self.cells:  # iterates through rows in self.cells
            for col in row:  # iterate through each column in row
                if col == 0:  # if column value is 0
                    return False  # returns False to indicate board is not full
        return True  # returns True if no empty cell is found

    def update_board(self):  # Phoebe H.
        for row in self.board:  # iterate through each row of 2D board
            for col in row:  # iterate through each column in row
                cell_2d_board = self.board[row][col]  # find cell in 2D board
                cell_object = self.cells[row][col]  # find corresponding Cell object in self.cells
                if cell_2d_board != cell_object.value:  # if 2D board cell differs from Cell object's value attribute,
                    cell_2d_board = cell_object.value  # update 2D board cell

    def find_empty(self):  # Vishakh S.
        for row in range(9):  # iterates through rows in Sudoku board
            for col in range(9):  # iterates through columns in Sudoku board
                if self.cells[row][col] == 0:  # if cell value is 0
                    return row, col  # returns row and col value to indicate empty cell
        return None  # returns None if no empty cells are available

    def check_board(self):  # Phoebe H.
        if self.board == self.correct_answer:  # if 2D board matches correct Sudoku board,
            return True  # return True
        return False  # otherwise, return False
