import numpy as np
import itertools


class Board:

    def __init__(self, width=5, height=5, mine_count=10):

        # Create array to hold which squares have mines
        empty_spaces = width * height - mine_count

        assert empty_spaces >= 0, 'You tried to add too many mines to a board.'

        self.mines = np.array([True] * mine_count + [False] * empty_spaces)
        np.random.shuffle(self.mines)
        self.mines = self.mines.reshape(height, width)

        # Count how many mines are adjacent to each square
        self.counts = np.zeros((height, width))

        def count_adjacent_mines(i, j):
            left = j - 1 if j > 0 else 0
            right = j + 2 if j < height - 1 else height

            top = i - 1 if i > 0 else 0
            bottom = i + 2 if i < width - 1 else width

            return self.mines[top:bottom, left:right].sum()

        for i, j in itertools.product(range(height), range(width)):
            self.counts[i, j] = count_adjacent_mines(i, j)

        # What to display to the user
        # -1 means a square has not been revealed yet.
        self.view = -np.ones((height, width))
