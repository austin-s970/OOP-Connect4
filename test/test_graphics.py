import unittest
from unittest.mock import MagicMock, Mock, patch
from hypothesis import given, settings, strategies, assume

from graphics import Color, Draw
from board import Spot, Board


class TestColor(unittest.TestCase):
    def setUp(self):
        """
        Setup function for 'TestColor'.
        This function sets up an instance
        of the 'Color' class to do tests
        on.
        """
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
        """
        Setup function for 'TestDraw'.
        This function sets up a mock
        board to do drawing tests on.
        """
        # Mocking the Board
        self.window = None
        self.mock_board = MagicMock(spec=Board)
        self.mock_board.height = 10
        self.mock_board.width = 10
        self.mock_board.__iter__.return_value = [
            (i // self.mock_board.width, i % self.mock_board.width,
             MagicMock()) for i in range(self.mock_board.height *
                                         self.mock_board.width)]
        self.mock_board.get_player_at_spot = Mock(
            side_effect=lambda x, y: None)
        self.mock_radius = Mock()

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
        expected_radius = int(self.draw.screen.square_size/2 - 5)
        self.assertEqual(self.draw.radius, expected_radius)

    @patch('pygame.draw.rect')
    def test_rectangle(self, mock_draw_rectangle) -> None:
        """
        Test the function for drawing
        rectangles.
        """
        # Create the expected rectangle parameters
        expected_color = (255, 0 , 0)  # Red
        draw_height = 1
        draw_width = 1

        # Define the dimensions of the expected rectangle
        expected_rectangle = (draw_width * self.draw.screen.square_size,
                              draw_height * self.draw.screen.square_size,
                              self.draw.screen.square_size,
                              self.draw.screen.square_size)

        # Call the method that is supposed to draw the rectangle
        self.draw.draw_rectangle(draw_height, draw_width, expected_color)

        # Assert that 'pygame.draw.rect' was called correctly
        mock_draw_rectangle.assert_called_once_with(self.draw.screen.window,
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
        mock_draw_circle.assert_called_once_with(self.draw.screen.window,
                                                 expected_color,
                                                 expected_center,
                                                 self.draw.radius)

    def test_gameboard_drawing(self) -> None:
        """
        Test the gameboard drawing function.
        """
        # Mock the 'draw_rectangle' function
        with (patch.object(self.draw, 'draw_rectangle') as mock_draw_rectangle,
              # Mock the 'draw_circle' function
              patch.object(self.draw, 'draw_circle') as mock_draw_circle,
              # Mock the 'pygame.display.update' function
              patch('pygame.display.update') as mock_update):
            # Mock the occupant status of the spots on the board
            self.mock_board.get_player_at_spot = Mock(return_value=None)

            # call the 'draw.gameboard' function to use for the
            # following tests
            self.draw.gameboard()

            # Check that 'draw_rectangle' was called the appropriate
            # number of times given the mocked board (10x10)
            self.assertEqual(mock_draw_rectangle.call_count, 100)

            # Check that 'draw_circle' was called the appropriate
            # number of times given the mocked board (10x10)
            self.assertEqual(mock_draw_circle.call_count, 100)

            # Check if any of the 'draw_circle' calls resulted in
            # an empty (black) circle
            empty_calls = [call for call in mock_draw_circle.call_args_list 
                           if call[0][0] == self.draw.color.black]

            # Assert that the number of empty circles was greater than 0
            self.assertGreater(len(empty_calls), 0)

            # Check that the pygame display was updated
            mock_update.assert_called_once()
