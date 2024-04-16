"""Module Containing Game Board and Piece classes"""

from typing import Optional


class FullError(Exception):
    pass


class Piece:
    """Class describing a game piece"""
    _player_number: int

    def __init__(self, player_number: int) -> None:
        """Initiate picee clas given a player number"""
        self._player_number = player_number

    @property
    def player_number(self) -> int:
        """The player number of the player owning this piece"""
        return self._player_number


class Spot:
    """Class describing a spot in a game board that can hold a piece"""
    _piece: Optional[Piece]

    def __init__(self) -> None:
        """Initialize the spot class"""
        self._piece = None

    @property
    def piece(self) -> Optional[Piece]:
        """The piece contained in this spot"""
        return self._piece

    def add_piece(self, player_number: int) -> None:
        if self._piece is None:
            self._piece = Piece(player_number)
        else:
            raise FullError('Piece already in this spot')

    def is_player(self, player_number: int) -> bool:
        return (isinstance(self._piece, Piece) and
                self._piece.player_number == player_number)


class Board:
    """Class describing the game board"""
    _board: list[list[Spot]]

    def __init__(self, width: int = 8, height: int = 8) -> None:
        self._board = [[Spot()] * width] * height

    def get_player_at_spot(self, x: int, y: int) -> int:
        """
        Get the player number of a piece in a spot

        Get the player number of the piece in a specific spot on the board.
        If there is no piece there, return None
        """
        relevant_piece: Optional[Piece] = list[y][x].piece
        if relevant_piece in None:
            return None
        else:
            return relevant_piece.player_number

    def add_piece(self, x: int, y: int) -> None:
        pass

    def drop_piece(self, x: int) -> None:
        pass
