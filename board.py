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

    def select(self, row, col):
        if self.selected is not None:
            self.selected = None

        self.selected = self.cells[row][col]

    def click(self, x, y):
        pass

    def clear(self):
        pass

    def sketch(self, value):
        pass

    def place_number(self, value):
        pass

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                original = self.board[row][col]

                if original != 0:
                    cell.set_cell_value(original)
                else:
                    cell.set_cell_value(0)
                    cell.set_sketched_value(0)

    def is_full(self):
        for row in self.cells:
            for col in row:
                if col == 0:
                    return False
        return True

    def update_board(self):  # Phoebe H.
        for row in self.board:  # iterate through each row of 2D board
            for col in row:  # iterate through each column in row
                cell_2d_board = self.board[row][col]  # find cell in 2D board
                cell_object = self.cells[row][col]  # find corresponding Cell object in self.cells
                if cell_2d_board != cell_object.value:  # if 2D board cell differs from Cell object's value attribute,
                    cell_2d_board = cell_object.value  # update 2D board cell

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col] == 0:
                    return row, col
        return None

    def check_board(self):  # Phoebe H.
        if self.board == self.correct_answer:  # if 2D board matches correct Sudoku board,
            return True  # return True
        return False  # otherwise, return False
