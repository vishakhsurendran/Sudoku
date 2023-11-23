import pygame
from constants import *


class Cell:
    def __init__(self, value, row, col, screen):  # Cell class constructor
        self.value = value
        self.sketched_value = 0  # initialize user-entered value to null object
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):  # setter for cell.value
        self.value = value

    def set_sketched_value(self, value):  # setter for cell.sketched_value
        self.sketched_value = value

    def draw(self):
        cell_font = pygame.font.Font(None, CELL_FONT)  # set font for numbers in cells

        if self.value:  # cell has provided value
            provided_number_surf = cell_font.render(str(self.value), 0, PROVIDED_NUMBER_COLOR)  # create number surface
            provided_number_rect = provided_number_surf.get_rect(  # create rectangle
                center=(self.col * CELL_SIZE + CELL_SIZE // 2, self.row * CELL_SIZE + CELL_SIZE // 2)  # center of cell
            )
            self.screen.blit(provided_number_surf, provided_number_rect)  # draw number to screen

        elif self.sketched_value:  # cell has sketched value
            sketched_number_surf = cell_font.render(str(self.sketched_value), 0, SKETCHED_NUMBER_COLOR)  # create number surface
            sketched_number_rect = sketched_number_surf.get_rect(  # create rectangle
                center=(self.col * CELL_SIZE + 16, self.row * CELL_SIZE + 16)  # top-left corner of cell
            )
            self.screen.blit(sketched_number_surf, sketched_number_rect)  # draw number to screen

        if self.selected:  # draw red outlines if cell is selected
            pygame.draw.line(  # draw top line of cell
                self.screen,
                RED_OUTLINE,
                (self.col * CELL_SIZE, self.row * CELL_SIZE),
                (self.col * CELL_SIZE + CELL_SIZE, self.row * CELL_SIZE),
                CELL_OUTLINE_WIDTH
            )
            pygame.draw.line(  # draw bottom line of cell
                self.screen,
                RED_OUTLINE,
                (self.col * CELL_SIZE, self.row * CELL_SIZE + CELL_SIZE),
                (self.col * CELL_SIZE + CELL_SIZE, self.row * CELL_SIZE + CELL_SIZE),
                CELL_OUTLINE_WIDTH
            )
            pygame.draw.line(  # draw left line of cell
                self.screen,
                RED_OUTLINE,
                (self.col * CELL_SIZE, self.row * CELL_SIZE),
                (self.col * CELL_SIZE, self.row * CELL_SIZE + CELL_SIZE),
                CELL_OUTLINE_WIDTH
            )
            pygame.draw.line(  # draw right line of cell
                self.screen,
                RED_OUTLINE,
                (self.col * CELL_SIZE + CELL_SIZE, self.row * CELL_SIZE),
                (self.col * CELL_SIZE + CELL_SIZE, self.row * CELL_SIZE + CELL_SIZE),
                CELL_OUTLINE_WIDTH
            )
