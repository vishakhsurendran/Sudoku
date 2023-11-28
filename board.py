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
        for row in range(9):
            arr = []
            for col in range(9):
                cell = Cell((0, row, col, screen))
                arr.append(cell)
            self.cells.append(arr)
        self.selected = None

    def draw(self):
        pass

    def select(self, row, col):  # Vishakh S.
        self.selected = self.cells[row][col]  # selects new cell using row and col values

    def click(self, x, y):
        pass

    def clear(self):
        pass

    def sketch(self, value):
        pass

    def place_number(self, value):
        pass

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
