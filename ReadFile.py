import random

class FileHandler:
    def __init__(self, fileName):
        self.fileName = fileName

    def read_file(self):
        # Read Sudoku Puzzles From File
        file = open(self.fileName, "r")

        # turn sudoku in a matrix
        counter = 0
        sudoku = []
        sudoku_list = []
        while True:
            line = file.readline().strip()

            if line == "":
                break
            if 1 <= counter < 10:
                sudoku.append([int(i) for i in line])
                if counter == 9:
                    sudoku_list.append(sudoku)
                    sudoku = []
                    counter = -1
            counter += 1

        which_sudoku = random.randrange(0, 50)
        sudoku = sudoku_list[which_sudoku]

        return sudoku