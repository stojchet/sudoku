import pygame
import sys
import math
import BacktrackingFinal as bt
import random
import copy
from enum import Enum
from ReadFile import FileHandler

# This function checks for a given number (with indices i j) whether it belongs to that position
# True - no error; False - error

class View:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.backtracker = bt.Backtracking(copy.deepcopy(sudoku))
        self.solved = self.backtracker.backtracking()
        self.grid = self.init_grid(sudoku)
        self.h = len(self.sudoku)
        self.w = len(self.sudoku[0])
        pygame.init()
        self.WIDTH = 700
        self.HEIGHT = 750
        self.COLOR_BACKGROUND = (230, 230, 225)
        self.COLOR_FIELD = (204, 153, 153)
        self.COLOR_ERROR = (250, 0, 0)
        self.COLOR_GREY = (105, 105, 105)
        self.COLOR_BOXES_BACKGROUND = (240, 230, 200)
        self.COLOR_DARKER = (160, 80, 100)
        self.COLOR_LIGHTER = (180, 160, 120)

        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.FONT = pygame.font.SysFont("Calibri", 35, True, False)
        self.MAIN_TEXT = self.FONT.render("Play a Game of Sudoku", True, self.COLOR_DARKER)
        self.BUTTON_TEXT_HINT = self.FONT.render("Hint", True, self.COLOR_BOXES_BACKGROUND)
        self.BUTTON_TEXT_DONE = self.FONT.render("Done", True, self.COLOR_BOXES_BACKGROUND)

        self.SIZE = 50
        self.MARGIN = 5
        self.BIG_MARGIN = (self.WIDTH - 9 * (self.SIZE + self.MARGIN) + self.MARGIN) // 2
        self.SUDOKU_SIZE = self.SIZE * 9 + self.MARGIN * 10

    def init_grid(self, sudoku):
        grid = [[0] * 9 for _ in range(9)]

        for i in range(9):
            for j in range(9):
                if sudoku[i][j] != 0:
                    grid[i][j] = self.Status.STATIC
                else:
                    grid[i][j] = self.Status.BLANK

        return grid

    def check_for_error(self, i, j):
        number = self.sudoku[i][j]
        valid_numbers = self.backtracker.valid(i, j)

        return number in valid_numbers

    def check_for_correctness(self):
        return self.sudoku == self.solved

    def give_hint(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.grid[i][j] == self.Status.BLANK:
                    self.grid[i][j] = self.Status.STATIC
                    self.sudoku[i][j] = self.solved[i][j]
                    return

    def helper_draw(self):
        square_size = (self.SIZE * int(math.sqrt(self.h)) + self.MARGIN * (int(math.sqrt(self.h)) - 1))
        for i in range(int(math.sqrt(self.h))):
            for j in range(int(math.sqrt(self.w))):
                left = self.BIG_MARGIN + (i % 3) * (square_size + self.MARGIN) + self.MARGIN
                up = 100 + (j % 3) * (square_size + self.MARGIN) + self.MARGIN
                pygame.draw.rect(self.surface, self.COLOR_LIGHTER, [left, up, square_size, square_size])

    class Status(Enum):
        BLANK = 0
        SELECTED = 1
        PUT_NUMBER = 2
        STATIC = 3
        ERROR = 4
        CORRECT = 5

    # 1 - selected field
    # 2 - put number in the selected field
    # 3 - static fields
    # 4 - error
    # 5 - correct
    def draw_grid(self):
        for i in range(9):
            for j in range(9):
                sq = pygame.Rect(self.BIG_MARGIN + i * (self.SIZE + self.MARGIN) + self.MARGIN, 100 + j * (self.SIZE + self.MARGIN) + self.MARGIN, self.SIZE, self.SIZE)

                # it has a number its not correct
                if self.sudoku[i][j] != self.Status.BLANK and self.grid[i][j] == self.Status.STATIC:
                    self.grid[i][j] = self.Status.STATIC
                    pygame.draw.rect(self.surface, self.COLOR_BOXES_BACKGROUND, sq)
                elif self.grid[i][j] == self.Status.ERROR:
                    bsq = pygame.Rect(self.BIG_MARGIN + i * (self.SIZE + self.MARGIN), 100 + j * (self.SIZE + self.MARGIN), self.SIZE + 2 * self.MARGIN,
                                      self.SIZE + 2 * self.MARGIN)
                    pygame.draw.rect(self.surface, self.COLOR_ERROR, bsq)
                    pygame.draw.rect(self.surface, self.COLOR_BOXES_BACKGROUND, sq)
                elif self.grid[i][j] == self.Status.CORRECT:
                    pygame.draw.rect(self.surface, self.COLOR_BOXES_BACKGROUND, sq)

                else:
                    if self.grid[i][j] == self.Status.SELECTED or self.grid[i][j] == self.Status.PUT_NUMBER:
                        pygame.draw.rect(self.surface, self.COLOR_FIELD, sq)
                    else:
                        pygame.draw.rect(self.surface, self.COLOR_BOXES_BACKGROUND, sq)

                # Displaying the numbers
                if self.grid[i][j] == self.Status.STATIC:
                    number = self.FONT.render(str(self.sudoku[i][j]), True, self.COLOR_GREY)
                    self.surface.blit(number, [self.MARGIN * 3 + (i + 2) * (self.SIZE + self.MARGIN), self.MARGIN + (j + 2) * (self.SIZE + self.MARGIN)])
                elif self.grid[i][j] == self.Status.ERROR or self.grid[i][j] == self.Status.PUT_NUMBER or self.grid[i][j] == self.Status.CORRECT:
                    number = self.FONT.render(str(self.sudoku[i][j]), True, (0, 0, 0))
                    self.surface.blit(number, [self.MARGIN * 3 + (i + 2) * (self.SIZE + self.MARGIN), self.MARGIN + (j + 2) * (self.SIZE + self.MARGIN)])

    def finished_game(self):
        if self.check_for_correctness():
            text = self.FONT.render("Your solution is correct", True, self.COLOR_DARKER)
            end_image = pygame.image.load(r'nt_smiley_transparent.png').convert_alpha()
            end_image = pygame.transform.scale(end_image, [430, 430])

        else:
            text = self.FONT.render("Your solution is incorrect", True, self.COLOR_DARKER)
            end_image = pygame.image.load(r'nt_sad_smiley_transparent.png').convert_alpha()
            end_image = pygame.transform.scale(end_image, [430, 430])

        button = self.FONT.render("Exit Game", True, self.COLOR_BOXES_BACKGROUND)
        while True:
            self.surface.fill(self.COLOR_BACKGROUND)
            self.surface.blit(text, [175, 535])
            self.surface.blit(end_image, [130, 50])

            # Exit Button
            pygame.draw.rect(self.surface, self.COLOR_LIGHTER, [260, 635, 175, 65])
            pygame.draw.rect(self.surface, self.COLOR_DARKER, [265, 640, 165, 55])
            self.surface.blit(button, [275, 650])

            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if 260 < mouse[0] < 440 and 635 < mouse[1] < 700:
                    sys.exit()

            pygame.display.flip()

    def mouse_button(self, row, col):
        hint = finish = is_error_selected = False
        mouse = pygame.mouse.get_pos()

        if 0 <= row <= 8 and 0 <= col <= 8:

            if self.grid[row][col] == self.Status.SELECTED:
                self.grid[row][col] = self.Status.BLANK

            elif self.grid[row][col] == self.Status.PUT_NUMBER:
                if not self.check_for_error(row, col):
                    self.grid[row][col] = self.Status.ERROR
                else:
                    self.grid[row][col] = self.Status.CORRECT

        pos = pygame.mouse.get_pos()

        if 160 < mouse[0] < 315 and 635 < mouse[1] < 700:
            hint = True
        elif 395 < mouse[0] < 550 and 635 < mouse[1] < 700:
            finish = True
        else:
            row = pos[0] // (self.SIZE + self.MARGIN) - 2
            col = pos[1] // (self.SIZE + self.MARGIN) - 2

            if 0 <= row <= 8 and 0 <= col <= 8:
                if self.grid[row][col] in [self.Status.ERROR, self.Status.CORRECT]:
                    if self.grid[row][col] == self.Status.ERROR:
                        is_error_selected = True
                    self.grid[row][col] = self.Status.PUT_NUMBER
                elif self.grid[row][col] == self.Status.BLANK:
                    self.grid[row][col] = self.Status.SELECTED

        return row, col, hint, finish, is_error_selected

    def key_down(self, ev_key, row, col, error_list, is_error_selected):
        key = chr(ev_key)

        if key.isnumeric():
            key = int(key)
            if self.grid[row][col] != self.Status.STATIC and isinstance(key, int):
                self.sudoku[row][col] = key
                if not self.check_for_error(row, col):
                    error_list.append([row, col])
                    self.grid[row][col] = self.Status.ERROR
                else:
                    self.grid[row][col] = self.Status.CORRECT

                if is_error_selected:
                    for er in error_list:
                        r, c = er[0], er[1]
                        if self.check_for_error(r, c):
                            self.grid[r][c] = self.Status.CORRECT
        elif ev_key == pygame.K_BACKSPACE:
            self.grid[row][col] = self.Status.BLANK
            self.sudoku[row][col] = 0

        if is_error_selected:
            is_error_selected = False

        return is_error_selected, error_list

    def draw_board(self):
        self.surface.fill(self.COLOR_BACKGROUND)
        self.surface.fill(self.COLOR_DARKER, rect=(self.BIG_MARGIN, 100, self.SUDOKU_SIZE, self.SUDOKU_SIZE))
        self.surface.blit(self.MAIN_TEXT, [190, 35])
        #                        upper left corner  len  height
        pygame.draw.rect(self.surface, self.COLOR_LIGHTER, [160, 635, 155, 65])
        pygame.draw.rect(self.surface, self.COLOR_DARKER, [165, 640, 145, 55])
        self.surface.blit(self.BUTTON_TEXT_HINT, [205, 650])

        pygame.draw.rect(self.surface, self.COLOR_LIGHTER, [395, 635, 155, 65])
        pygame.draw.rect(self.surface, self.COLOR_DARKER, [400, 640, 145, 55])
        self.surface.blit(self.BUTTON_TEXT_DONE, [435, 650])

    def run(self):
        col = row = 0
        hint = is_error_selected = finish = False
        error_list = []

        while True:
            self.draw_board()

            if hint:
                self.give_hint()
                hint = False

            if finish:
                break

            self.helper_draw()
            self.draw_grid()

            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()

            # selecting a field
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col, hint, finish, is_error_selected = self.mouse_button(row, col)

            # entering a value
            elif event.type == pygame.KEYDOWN:
                is_error_selected, error_list = self.key_down(event.key, row, col, error_list, is_error_selected)

            pygame.display.flip()

        self.finished_game()


def __main__():
    fileHandler = FileHandler("sudoku_puzzles.txt")
    sudoku = fileHandler.read_file()

    game = View(sudoku)
    game.run()

__main__()