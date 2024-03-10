import unittest
from hypothesis import given, strategies

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
