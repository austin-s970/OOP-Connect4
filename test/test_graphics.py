import unittest
from unittest.mock import Mock, patch
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
        self.window = None
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

    def test_radius_getter(self) -> None:
        """
        Test the getter method for
        the radius of the circles.
        """
        expected_radius = int(self.draw.square_size/2 - 5)
        self.assertEqual(self.draw.radius, expected_radius)
    
    @patch('pygame.draw.rect')
    def test_rectangle(self, mock_draw_rectangle) -> None:
        """
        Test the function for drawing
        rectangles.
        """
        # Create the expected rectangle parameters
        expected_color = (255, 0 , 0) # Red
        draw_height = 1
        draw_width = 1

        # Define the dimensions of the expected rectangle
        expected_rectangle = (draw_width * self.draw.square_size,
                              draw_height * self.draw.square_size,
                              self.draw.square_size,
                              self.draw.square_size)

        # Call the method that is supposed to draw the rectangle
        self.draw.draw_rectangle(draw_height, draw_width, expected_color)

        # Assert that 'pygame.draw.rect' was called correctly
        mock_draw_rectangle.assert_called_once_with(self.draw.window,
                                                    expected_color, 
                                                    expected_rectangle)

    @patch('pygame.draw.circle')
    def test_circle(self, mock_draw_circle) -> None:
        """
        Test the function for drawing
        circles.
        """
        # Create the expected circle parameters
        expected_color = (0, 0, 255)  # Blue
        expected_center = (100, 100)

        # Call the method that is supposed to draw the circle
        self.draw.draw_circle(expected_color, expected_center)

        # Assert that pygame.draw.circle was called correctly
        mock_draw_circle.assert_called_once_with(self.draw.window,
                                                 expected_color, 
                                                 expected_center, 
                                                 self.draw.radius)
