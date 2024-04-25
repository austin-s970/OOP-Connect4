"""Module Containing Game Board and Piece classes."""
from typing import Optional, Iterator

import pygame


class FullError(Exception):
    """
    Custom exception to handle
    the case that the board is full.
    """
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


class BoardIterator:
    _x: int = 0
    _y: int = 0

    _board: list[list[Spot]]
    _width: int
    _height: int

    def __init__(self, board: list[list[Spot]]) -> None:
        self._board = board
        self._width = len(board[0])
        self._height = len(board)

    def __iter__(self) -> Iterator[tuple[int, int, Spot]]:
        return self

    def __next__(self) -> tuple[int, int, Spot]:
        if self._x >= self._width:
            self._x = 0
            self._y += 1
        if self._y >= self._height:
            raise StopIteration
        return_val: tuple[int, int, Spot] = (self._y, self._x,
                                             self._board[self._y][self._x])
        self._x += 1
        return return_val


class Board(Screen):
    """Class describing the game board."""
    _board: list[list[Spot]]

    def __init__(self, cols: int = 7, rows: int = 6) -> None:
        """
        Constructor for the board.
        """
        self._rows = rows
        self._cols = cols
        super().__init__(rows, cols)
        self._spot = Spot()
        self._board = [[Spot() for i in range(cols)] for j in range(rows)]

    def __iter__(self) -> Iterator[tuple[int, int, Spot]]:
        return BoardIterator(self._board)

    @property
    def spot(self) -> Spot:
        """
        getter property for a spot on the board

        Returns:
            Spot: an instance of the 'Spot' class.
        """
        return self._spot

    @property
    def rows(self) -> int:
        """
        getter property for the rows

        Returns:
            int: the integer count for rows.
        """
        return self._rows

    @property
    def cols(self) -> int:
        """
        getter property for the columns

        Returns:
            int: the integer count for columns.
        """
        return self._cols

    def reset(self) -> None:
        """
        Function to reset the board in the event
        of a replay.
        """
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
        """
        getter property for the board width

        Returns:
            int: the integer value for the board width.
        """
        return len(self._board[0])

    @property
    def height(self) -> int:
        """
        getter property for the board height

        Returns:
            int: the integer value for the board height.
        """
        return len(self._board)

    def drop_piece(self, x: int, player_number: int) -> None:
        if not (x >= 0 and x < self.window_width):
            raise ValueError
        for y in range(self.height):
            if self._board[y][x].is_empty():
                self._board[y][x].add_piece(player_number)
                break
        else:
            raise FullError

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
        # Check for positive diagonals (bottom-left to top-right)
        for y in range(self.height - 3):
            for x in range(self.width - 3):
                if all(self.is_player(x + i, y + i,
                                      player_number) for i in range(4)):
                    return True

        # Check for negative diagonals (top-left to bottom-right)
        for y in range(3, self.height):
            for x in range(self.width - 3):
                if all(self.is_player(x + i, y - i,
                                      player_number) for i in range(4)):
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
