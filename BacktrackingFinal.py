import math

class Backtracking:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.h = len(sudoku)
        self.w = len(sudoku[0])

    @property
    def range_for_boxes(self):
        return self.h // int(math.sqrt(self.h))

    def determine_box_3x3(self, i, j):
        box_range = self.range_for_boxes
        return i // box_range, j // box_range

    def valid(self, i, j):
        temp = set(range(1, 10))

        # determine in which of the 9 boxes the number is placed
        row_box_index, col_box_index = self.determine_box_3x3(i, j)
        temp -= {self.sudoku[r][c] for r in range(row_box_index * 3, (row_box_index + 1) * 3)
                 for c in range(col_box_index * 3, (col_box_index + 1) * 3)
                 if (r, c) != (i, j)}

        # check in row
        temp -= {self.sudoku[m][j] for m in range(self.w) if m != i}

        # check in column
        temp -= {self.sudoku[i][m] for m in range(self.w) if m != j}

        return temp

    # return possible actions - numbers to be put at a certain index i, j
    # use filter/enumerate
    def actions(self):
        for i in range(len(self.sudoku)):
            for j in range(len(self.sudoku[i])):
                if self.sudoku[i][j] == 0:
                    temp = self.valid(i, j)
                    return temp, i, j

    def backtracking(self):
        temp = self.actions()
        if temp is None:
            return self.sudoku

        list_of_actions, i, j = temp

        for action in list_of_actions:
            self.sudoku[i][j] = action
            if self.backtracking():
                return self.sudoku

            self.sudoku[i][j] = 0

        return False
