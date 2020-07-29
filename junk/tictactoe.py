"""Josh's small Tic Tac Toe example (for practice!).

I'll reimplement it in Rust later for even more fun and profit!"""

import numpy as np
from enum import Enum


class TTTState(Enum):
    NO_WIN = 0x0
    X_WIN = 0x1
    O_WIN = 0x2
    DRAW = 0x3


class Tictactoe:
    def __init__(self):
        self.reset()
        self._x_win = 0
        self._o_win = 0
        self._draw = 0

    def convert(self, player: str):
        if player == "x" or player == "X":
            return 1
        elif player == "o" or player == "O":
            return 2
        else:
            raise ValueError

    def reset(self):
        self._board = np.zeros([3, 3], dtype=int)
        self._turn_count = 0
        self._victory = TTTState.NO_WIN

    def move(self, x: int, y: int, player: int):
        if self.board[y][x] != 0:
            raise ValueError
        else:
            self.board[y][x] = player

    def check_all_horizontal(self):
        for array in len(range(self._board)):
            if array == 1:
                self._victory |= TTTState.X_WIN
            elif array == 2:
                self._victory |= TTTState.O_WIN

    def check_all_vertical(self):
        pass

    def check_win(self):
        self.check_all_horizontal()
        self.check_all_vertical()

