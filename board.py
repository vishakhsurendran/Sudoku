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
    pass
