"""Module Containing Game Board and Piece classes."""

import pygame
from typing import Optional


class FullError(Exception):
    pass


class Screen():
    def __init__(self, rows: int, cols: int) -> None:
        """
        Constructor for 'Screen'.
        """
        self._square_size = 100
        self._window_width = cols * self._square_size
        self._window_height = (rows+1) * self._square_size
        self._window_size = (self._window_width, self._window_height)
        self._window = pygame.display.set_mode(self._window_size)

    @property
    def window(self) -> pygame.Surface:
        """
        getter property for the screen window

        Returns:
            pygame.Surface: an instance of pygame's 'Surface' class.
        """
        return self._window

    @property
    def window_size(self) -> tuple[int, int]:
        """
        getter property for the screen window's size

        Returns:
            tuple[int, int]: 'x' and 'y' values representing the
            and height of the screen window.
        """
        return self._window_size

    @property
    def square_size(self) -> int:
        """
        getter property for the square size

        Returns:
            int: an integer representing the square size.
        """
        return self._square_size

    @property
    def window_width(self) -> int:
        """
        getter property for the screen window width

        Returns:
            int: an integer representing the window width.
        """
        return self._window_width

    @property
    def window_height(self) -> int:
        """
        getter property for the screen window height

        Returns:
            int: an integer representing the window height.
        """
        return self._window_height


class Piece:
    """Class describing a game piece."""
    _player_number: int

    def __init__(self, player_number: int) -> None:
        """Initiate piece class given a player number."""
        self._player_number = player_number

    @property
    def player_number(self) -> int:
        """The player number of the player owning this piece."""
        return self._player_number


class Spot:
    """Class describing a spot in a game board that can hold a piece."""
    _piece: Optional[Piece]

    def __init__(self) -> None:
        """Initialize the spot class."""
        self._piece = None

    @property
    def piece(self) -> Optional[Piece]:
        """The piece contained in this spot."""
        return self._piece

    def is_empty(self) -> bool:
        return self._piece is None

    def add_piece(self, player_number: int) -> None:
        if self._piece is None:
            self._piece = Piece(player_number)
        else:
            raise FullError('Piece already in this spot')

    def is_player(self, player_number: int) -> bool:
        return (isinstance(self._piece, Piece) and
                self._piece.player_number == player_number)

    def player_number(self) -> int:
        if self._piece is None:
            return 0
        else:
            return self._piece.player_number


class Board(Screen):
    """Class describing the game board."""
    _board: list[list[Spot]]

    def __init__(self, cols: int = 7, rows: int = 6) -> None:
        self._rows = rows
        self._cols = cols
        super().__init__(rows, cols)
        self._spot = Spot()
        self._board = [[Spot() for i in range(cols)] for j in range(rows)]

    @property
    def spot(self) -> None:
        return self._spot

    @property
    def rows(self) -> None:
        return self._rows

    @property
    def cols(self) -> None:
        return self._cols

    def reset(self) -> None:
        for row in self._board:
            for spot in row:
                spot._piece = None

    def get_player_at_spot(self, x: int, y: int) -> int:
        """
        Get the player number of the piece in a specific spot on the board.
        If there is no piece there, return None.
        """
        relevant_piece: Optional[Piece] = self._board[y][x].piece
        if relevant_piece is None:
            return 0
        else:
            return relevant_piece.player_number

    @property
    def width(self) -> int:
        return len(self._board[0])

    @property
    def height(self) -> int:
        return len(self._board)

    def drop_piece(self, x: int, player_number: int) -> None:
        if not (x >= 0 and x < self.window_width):
            raise ValueError
        for y in range(self.window_height):
            if self._board[y][x].is_empty():
                self._board[y][x].add_piece(player_number)
                break
        else:
            raise FullError

    def __str__(self) -> str:
        return_val: str = ''
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                player_num = self.get_player_at_spot(x, y)
                if player_num == 1:
                    return_val += 'X'
                elif player_num == 2:
                    return_val += 'O'
                else:
                    return_val += ' '
            return_val += '\n'
        return_val += ''.join([str(i + 1) for i in range(self.width)])
        return return_val

    def is_player(self, x: int, y: int, player_number: int) -> bool:
        """
        Check if a player is in a specific location

        Check if a player number matches the x and y passed, returning true
        if it does, and false in all other cases.
        """
        return (x >= 0 and x < self.width and y >= 0 and y < self.height and
                self._board[y][x].is_player(player_number))

    def _diagonal_win(self, player_number: int) -> bool:
        """
        Check for a diagonal win.
        Return true if it has occurred, false if not.
        """
        for y in range(self.height):
            for x in range(self.width):
                # positive diagonals
                for xy1 in range(y + 1, y + 4):
                    if not self.is_player(x + xy1, y + xy1, player_number):
                        break
                else:
                    return True
                # negative diagonals
                for xy2 in range(y + 1, y + 4):
                    if not self.is_player(x - xy2, y + xy2, player_number):
                        break
                else:
                    return True
        return False

    def has_won(self, player_number: int) -> bool:
        """
        Check if a player has won, returning true if they have and false if not
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.is_player(x, y, player_number):
                    # horizontal
                    for x2 in range(x + 1, x + 4):
                        if not self.is_player(x2, y, player_number):
                            break
                    else:
                        return True
                    # vertical
                    for y2 in range(y + 1, y + 4):
                        if not self.is_player(x, y2, player_number):
                            break
                    else:
                        return True
                    if self._diagonal_win(player_number):
                        return True
        return False
