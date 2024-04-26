import unittest
from unittest.mock import patch

from main import main


class TestMain(unittest.TestCase):
    @patch('game.Game.game_loop')
    def test_main(self, mock_loop):
        """
        Test that the game loop is
        called once in the main
        module.
        """
        main()

        # Check that the 'game_loop function
        # was called once main was called.
        mock_loop.assert_called_once()
