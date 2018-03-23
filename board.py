import numpy as np
import itertools
from queue import Queue


class Board:

    def __init__(self, width=5, height=5, mine_count=2):
        self.width = width
        self.height = height
        self.mine_count = mine_count

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
            right = j + 2 if j < width - 1 else width
            top = i - 1 if i > 0 else 0
            bottom = i + 2 if i < height - 1 else height

            return self.mines[top:bottom, left:right].sum()

        for i, j in itertools.product(range(height), range(width)):
            self.counts[i, j] = count_adjacent_mines(i, j)

        # What to display to the user
        # -1 means a square has not been revealed yet.
        self.view = -np.ones((height, width))

    def reveal(self, i, j):
        """
        Reveal a square of the board. If the square contains a zero, also reveal adjacent squares.
        Continue like this until there are no more squares to reveal.
        This is implemented using a queue, instead of recursively.
        """

        if self.counts[i, j] != 0:
            self.view[i, j] = self.counts[i, j]
        else:
            q = Queue()
            q.put((i, j))

            while not q.empty():
                i, j = q.get_nowait()

                left = j - 1 if j > 0 else 0
                right = j + 2 if j < self.width - 1 else self.width
                top = i - 1 if i > 0 else 0
                bottom = i + 2 if i < self.height - 1 else self.height

                for _i, _j in itertools.product(range(top, bottom), range(left, right)):
                    if self.counts[_i, _j] == 0 and self.view[_i, _j] == -1:
                        q.put_nowait((_i, _j))
                    self.view[_i, _j] = self.counts[_i, _j]

    def score(self):
        """
        The current player's score. This is just the number of revealed squares.
        If the player has won, they also receive one point per mine.
        :return:
        """

        score = (self.view != -1).sum()

        if score == self.width * self.height - self.mine_count:
            score = self.width * self.height

        return score

    def game_won(self):
        return self.score() == self.width * self.height

    def any_mines_revealed(self):
        showing_mines = self.mines & (self.view != -1)
        return showing_mines.any()