import unittest
from unittest.mock import patch, MagicMock
from hypothesis import given, strategies

from game import Game
from graphics import MultiError


class TestGame(unittest.TestCase):
    @given(board_width=strategies.integers(),
           board_height=strategies.integers())
    def test_init_and_properties(self, board_width: int, board_height: int
                                 ) -> None:
        """test the init function"""
        with (patch('game.Turns') as Turns,
              patch('game.Board') as Board,
              patch('game.Screen') as Screen,
              patch('game.Color') as Color,
              patch('game.Draw') as Draw):
            Board().height = board_height
            Board().width = board_width
            game = Game()
            self.assertEqual(game.turn, Turns())
            self.assertEqual(game.board, Board())
            Screen.assert_called_with(board_height, board_width)
            self.assertEqual(game.screen, Screen())
            self.assertEqual(game.color, Color())
            self.assertEqual(game.draw, Draw())
            self.assertEqual(game._draw2, Draw())

    def test_init_singleton_check(self) -> None:
        with (patch('game.Turns'), patch('game.Board'), patch('game.Screen'),
              patch('game.Color'), patch('game.Draw') as Draw):
            Draw.side_effect = [MagicMock(), MagicMock()]
            self.assertRaises(MultiError, Game)

    @given(strategies.integers(min_value=1, max_value=2))
    def test_print_winner_message(self, player_number: int) -> None:
        with (patch('game.Turns'), patch('game.Board'),
              patch('game.Screen') as Screen,
              patch('game.Color') as Color, patch('game.Draw'),
              patch('game.pygame') as pygame):
            font = pygame.font.SysFont()
            expected_message: str = f"Player {player_number} wins!"
            expected_color: MagicMock
            if player_number == 1:
                expected_color = Color().red
            elif player_number == 2:
                expected_color = Color().yellow
            else:
                expected_color = MagicMock()
            game = Game()
            game._print_winner_message(player_number)
            font.render.assert_called_with(
                expected_message, 1, expected_color)
            Screen().window.blit.assert_called()

    def test_print_tie_message(self) -> None:
        with (patch('game.Turns'), patch('game.Board'),
              patch('game.Screen') as Screen,
              patch('game.Color') as Color, patch('game.Draw'),
              patch('game.pygame') as pygame):
            font = pygame.font.SysFont()
            expected_message: str = "Tie Game!"
            expected_color = Color().blue
            game = Game()
            game._print_tie_message()
            font.render.assert_called_with(expected_message, 1, expected_color)
            Screen().window.blit.assert_called()

    @given(xpos=strategies.integers(min_value=0, max_value=1000),
           square_size=strategies.integers(min_value=1, max_value=100),
           player_turn=strategies.integers(min_value=1, max_value=2))
    def test_handle_mouse_motion(self, xpos: int, square_size: int,
                                 player_turn: int) -> None:
        with (patch('game.Turns') as Turns, patch('game.Board'),
              patch('game.Screen'),
              patch('game.Color') as Color, patch('game.Draw') as Draw,
              patch('game.pygame')):
            Turns()._player_turn = player_turn
            Draw().screen.square_size = square_size
            expected_color: MagicMock() = Color().black
            screen: MagicMock = MagicMock()
            event_pos = [xpos]
            game = Game()
            game.handle_mouse_motion(screen, event_pos)
            screen.fill.assert_called_with(expected_color)
            if player_turn == 1:
                expected_color = Color().red
            elif player_turn == 2:
                expected_color = Color().yellow
            Draw().draw_circle.assert_called_once_with(
                expected_color, (xpos, int(square_size / 2)))
