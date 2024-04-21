import unittest
from unittest.mock import Mock
from hypothesis import given, settings, strategies, assume

from graphics import Color, Draw
from board import Spot, Board


class TestColor(unittest.TestCase):
    def setUp(self):
        self.color = Color()

    def test_red_getter(self) -> None:
        """
        Test the getter method
        for the color 'red'.
        """
        expected_color = (255, 0, 0)
        self.assertEqual(self.color.red, expected_color)

    def test_blue_getter(self) -> None:
        """
        Test the getter method
        for the color 'blue'.
        """
        expected_color = (0, 0, 255)
        self.assertEqual(self.color.blue, expected_color)

    def test_yellow_getter(self) -> None:
        """
        Test the getter method
        for the color 'yellow'.
        """
        expected_color = (255, 255, 0)
        self.assertEqual(self.color.yellow, expected_color)

    def test_lightblue_getter(self) -> None:
        """
        Test the getter method
        for the color 'lightblue'.
        """
        expected_color = (0, 255, 255)
        self.assertEqual(self.color.lightblue, expected_color)

    def test_black_getter(self) -> None:
        """
        Test the getter method
        for the color 'black'.
        """
        expected_color = (0, 0, 0)
        self.assertEqual(self.color.black, expected_color)

class TestDraw(unittest.TestCase):
    def setUp(self):
        # Mocking the Board
        self.mock_board = Mock(spec=Board)
        self.mock_board.height = 10
        self.mock_board.width = 10

        # Initialize Draw with the mock board
        self.draw = Draw(self.mock_board)

    def test_board_getter(self) -> None:
        """
        Test the getter method for
        the board.
        """
        self.assertIs(self.draw.board, self.mock_board)

    def test_spot_getter(self) -> None:
        """
        Test the getter method for
        a spot on the board.
        """
        self.assertIsInstance(self.draw.spot, Spot)

    def test_color_getter(self) -> None:
        """
        Test the getter method for
        a color.
        """
        self.assertIsInstance(self.draw.color, Color)

    def test_radius_getter(self):
        """
        Test the getter method for
        the radius of the circles.
        """
        expected_radius = int(self.draw.square_size/2 - 5)
        self.assertEqual(self.draw.radius, expected_radius)