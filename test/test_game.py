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

    @given(screen_width=strategies.integers(10, 1000),
           square_size=strategies.integers(5, 200))
    def test_print_replay_message(self, screen_width: int, square_size: int
                                  ) -> None:
        with (patch('game.Turns'), patch('game.Board'),
              patch('game.Screen') as Screen,
              patch('game.Color') as Color, patch('game.Draw'),
              patch('game.pygame') as pygame):
            Screen().window_width = screen_width
            Screen().square_size = square_size
            font = pygame.font.SysFont()
            expected_background_color = Color().black
            expected_text_color = Color().lightblue
            game = Game()
            game._print_replay_message()
            pygame.draw.rect.assert_called_with(
                Screen().window, expected_background_color,
                (0, 0, screen_width, square_size))
            font.render.assert_called_once()
            positional, keyword = font.render.call_args
            self.assertEqual(len(positional), 3)
            self.assertIsInstance(positional[0], str)
            self.assertEqual(positional[1], 1)
            self.assertEqual(positional[2], expected_text_color)
            self.assertEqual(keyword, {})
            label = font.render()
            Screen().window.blit.assert_called_with(label, (20, 5))

    def test_replay(self) -> None:
        with (patch('game.Turns'), patch('game.Board'),
              patch('game.Screen'),
              patch('game.Color'), patch('game.Draw'),
              patch('game.pygame') as pygame, patch('game.sys') as sys):
            print_replay_message = MagicMock()
            event = MagicMock()
            game = Game()
            game._print_replay_message = print_replay_message
            event_return_vals = [[MagicMock()] for i in range(20)]
            event_return_vals[0][0].type = pygame.MOUSEBUTTONDOWN
            event_return_vals[2][0].type = pygame.KEYDOWN
            event_return_vals[3][0].type = pygame.KEYDOWN
            event_return_vals[3][0].key = pygame.K_ESCAPE
            event_return_vals[4][0].type = pygame.QUIT
            event_return_vals[5][0].type = pygame.MOUSEBUTTONDOWN
            pygame.event.get.side_effect = event_return_vals
            self.assertTrue(game._replay(event))
            print_replay_message.assert_called_once_with()
            pygame.display.update.assert_called_once_with()
            pygame.time.delay.assert_not_called()
            event.assert_not_called()
            self.assertFalse(game._replay(event))
            pygame.quit.assert_not_called()
            sys.exit.assert_not_called()
            pygame.time.delay.assert_called
            self.assertTrue(game._replay(event))
            pygame.quit.assert_called_once_with()
            sys.exit.assert_called_once_with()

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

    @given(xpos=strategies.floats(min_value=0, max_value=1000, allow_nan=False,
                                  allow_infinity=False),
           square_size=strategies.integers(1, 200))
    def test_handle_mouse_click_noerror_noend(self, xpos: float,
                                              square_size: int) -> None:
        with (patch('game.Turns') as Turns, patch('game.Board') as Board,
              patch('game.Screen') as Screen,
              patch('game.Color') as Color, patch('game.Draw') as Draw,
              patch('game.pygame') as pygame):
            Screen().square_size = square_size
            Board().has_won.return_value = False
            Turns()._turn_count = 41
            game: Game = Game()
            event_pos = [xpos, 2.6]
            self.assertIsNone(game.handle_mouse_click(event_pos))
            expected_top_color: MagicMock() = Color().black
            pygame.draw.rect.assert_called_once_with(
                Screen().window, expected_top_color,
                (0, 0, Screen().window_width, square_size))
            correct_column: int = int(xpos / square_size)
            Board().drop_piece.assert_called_once_with(correct_column,
                                                       Turns()._player_turn)
            Draw().gameboard.assert_called_once_with()
            pygame.display.update.assert_called_once_with()
            Turns()._increment_turn.assert_called_once_with()
            Turns()._switch_player.assert_called_once_with()

    @given(xpos=strategies.floats(min_value=0, max_value=1000, allow_nan=False,
                                  allow_infinity=False))
    def test_handle_mouse_click_winner(self, xpos: float) -> None:
        with (patch('game.Turns') as Turns, patch('game.Board') as Board,
              patch('game.Screen'),
              patch('game.Color'), patch('game.Draw'),
              patch('game.pygame') as pygame):
            Board().has_won.return_value = True
            game = Game()
            game._print_winner_message = MagicMock()
            self.assertEqual(game.handle_mouse_click([xpos, 5.4]),
                             pygame.time.get_ticks())
            game._print_winner_message.assert_called_once_with(
                Turns()._player_turn)

    def test_game_loop(self) -> None:
        with (patch('game.Turns'), patch('game.Board') as Board,
              patch('game.Screen'),
              patch('game.Color'), patch('game.Draw') as Draw,
              patch('game.pygame') as pygame):
            handle_mouse_click = MagicMock()
            replay = MagicMock()
            replay.side_effect = [True, False]
            handle_mouse_click.side_effect = [7, None, 2, None, 6, None, 6, 6]
            pygame.time.get_ticks.side_effect = [2000, 4000, 4000, 4000, 4000]
            event_side_effect = [[MagicMock()] for i in range(200)]
            event_side_effect[0][0].type = pygame.MOUSEBUTTONDOWN
            event_side_effect[1][0].type = pygame.MOUSEMOTION
            event_side_effect[2][0].type = pygame.MOUSEBUTTONDOWN
            event_side_effect[3][0].type = pygame.MOUSEBUTTONDOWN
            event_side_effect[4][0].type = pygame.MOSUEBUTTONDOWN
            event_side_effect[5][0].type = pygame.MOUSEBUTTONDOWN
            pygame.event.get.side_effect = event_side_effect
            game = Game()
            game.handle_mouse_click = handle_mouse_click
            game._replay = replay
            game.game_loop()
            pygame.init.assert_called()
            Draw().gameboard.assert_called()
            pygame.display.update.assert_called()
            handle_mouse_click.assert_called()
            replay.assert_called()
            Board().reset.assert_called()
            Draw().gameboard.assert_called()
            pygame.time.Clock().tick.assert_called()
            pygame.display.update.assert_called()
