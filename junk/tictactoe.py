"""Please, Mr. Linter, stop yelling about doc strings and the neighbors."""

import numpy as np
from enum import Enum


class TTTState(Enum):
    """Enumeration for tic-tac-toe conditions."""

    NO_WIN = 0x0
    X_WIN = 0x1
    O_WIN = 0x2
    DRAW = 0x3


class Tictactoe:
    """Silly tic-tac-toe project. I don't even like tic-tac-toe."""

    def __init__(self):
        self.reset()
        self._x_win = 0
        self._o_win = 0
        self._draw = 0

    def convert(self, player: str):
        """Convert string -> TTTState."""
        if player == "x" or player == "X":
            return TTTState.X_WIN
        elif player == "o" or player == "O":
            return TTTState.O_WIN
        else:
            raise ValueError

    def reset(self):
        """Reset the board to a base state."""
        self._board = np.zeros([3, 3], dtype=int)
        self._turn_count = 0
        self._victory = TTTState.NO_WIN

    def move(self, x: int, y: int, player: int):
        """Validate and perform a player's move."""
        if self.board[y][x] != 0:
            raise ValueError
        else:
            self.board[y][x] = player

    def check_flat(self, array: np.ndarray()):
        """Check a one dimensional array for a win state."""
        if array == TTTState.X_WIN:
            self._victory |= TTTState.X_WIN
        elif self._victory == TTTState.O_WIN:
            self._victory |= TTTState.O_WIN

    def _check_win(self):
        consume = list(map(self.check_flat, self._board))
        consume = list(map(self.check_flat), self._board.transpose())
        self.check_flat(self._board.diagonal())

    def print_board(self):
        pass

    def get_input(self):
        pass

    def play(self):
        self.print_board()
        self.get_input()
        #self.
