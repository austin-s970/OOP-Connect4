import unittest
from hypothesis import given, settings, strategies, assume

import board


class TestPiece(unittest.TestCase):

    @given(player_number=strategies.integers())
    def test_init_and_player_number(self, player_number) -> None:
        piece = board.Piece(player_number)
        self.assertEqual(piece.player_number, player_number)


class TestSpot(unittest.TestCase):

    spot: board.Spot

    def setUp(self) -> None:
        self.spot = board.Spot()

    def test_init(self) -> None:
        self.assertIsNone(self.spot.piece)

    def test_piece_getter(self) -> None:
        piece = board.Piece(1)
        self.spot._piece = piece
        self.assertEqual(self.spot.piece, piece)

    @given(first=strategies.integers(), second=strategies.integers())
    def test_add_piece(self, first, second) -> None:
        self.spot = board.Spot()
        self.assertIsNone(self.spot.piece)
        self.spot.add_piece(first)
        self.assertIsNotNone(self.spot.piece)
        self.assertEqual(self.spot.piece.player_number, first)
        self.assertRaises(board.FullError, self.spot.add_piece, second)

    @given(playernum=strategies.integers())
    def test_is_player_empty(self, playernum: int) -> None:
        self.spot = board.Spot()
        self.assertFalse(self.spot.is_player(playernum))

    @given(first=strategies.integers(), second=strategies.integers())
    def test_is_player_nonempty(self, first: int, second: int) -> None:
        self.spot = board.Spot()
        self.spot.add_piece(first)
        self.assertEqual(self.spot.is_player(second), first == second)


class TestBoard(unittest.TestCase):

    board: board.Board

    # No deadline was a temporary change to satisfy CI/CD
    @settings(deadline=None)
    @given(x=strategies.integers(0, 6), y=strategies.integers(0, 5))
    def test_init_empty(self, x, y) -> None:
        self.board = board.Board()
        self.assertEqual(len(self.board._board), 6)
        self.assertEqual(len(self.board._board[y]), 7)
        self.assertIsInstance(self.board._board[y][x], board.Spot)

    # No deadline was a temporary change to satisfy CI/CD
    # @settings(deadline=None)
    # @given(width=strategies.integers(1, 100),
    #        height=strategies.integers(1, 100),
    #        x=strategies.integers(0, 100),
    #        y=strategies.integers(0, 100))
    # def test_init_args(self, width: int, height: int, x: int, y: int) -> None:
    #     assume(x < width)
    #     assume(y < height)
    #     self.board = board.Board(width, height)
    #     self.assertEqual(len(self.board._board), height)
    #     self.assertEqual(len(self.board._board[y]), width)
    #     self.assertIsInstance(self.board._board[y][x], board.Spot)
