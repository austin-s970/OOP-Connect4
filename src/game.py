"""
Module containing the Game Mediator Class
"""

from typing import Optional

import pygame
import sys
import math

from graphics import Color, Draw, MultiError
from board import Screen, Board, FullError
from turns import Turns


class Game():
    """
    Game mediator class
    """
    def __init__(self) -> None:
        """
        constructor
        """
        self._turn: Turns = Turns()
        self._board: Board = Board()
        self._screen: Screen = Screen(self._board.height, self._board.width)
        self._color: Color = Color()
        self._draw: Draw = Draw(self._board)
        self._draw2: Draw = Draw(self._board)

        # Verify that 'Draw' is a singleton class
        if id(self._draw) != id(self._draw2):
            raise MultiError
        else:
            pass

    @property
    def turn(self) -> Turns:
        """
        getter property for the board

        Returns:
            Board: an instance of the 'Board' class.
        """
        return self._turn

    @property
    def board(self) -> Board:
        """
        getter property for the board

        Returns:
            Board: an instance of the 'Board' class.
        """
        return self._board

    @property
    def screen(self) -> Screen:
        """
        getter property for the screen

        Returns:
            Screen: an instance of the 'Screen' class.
        """
        return self._screen

    @property
    def color(self) -> Color:
        """
        getter property for a color

        Returns:
            Color: an instance of the 'Color' class.
        """
        return self._color

    @property
    def draw(self) -> Draw:
        """
        getter property for drawing functionality.

        Returns:
            Draw: an instance of the 'Draw' class.
        """
        return self._draw

    def _print_winner_message(self, player: int) -> None:
        """
        function to print the message if a player wins.
        """
        font = pygame.font.SysFont("monospace", 75)
        message: str = "Player " + str(player) + " wins!"
        if player == 1:
            color = self.color.red
            label = font.render(message, 1, color)
            self.screen.window.blit(label, (40, 10))
        else:
            color = self.color.yellow
            label = font.render(message, 1, color)
            self.screen.window.blit(label, (40, 10))
        print(message)

    def _print_tie_message(self) -> None:
        """
        funcion to print the message if the players tie
        """
        font = pygame.font.SysFont("monospace", 75)
        message: str = "Tie Game!"
        color = self.color.blue
        label = font.render(message, 1, color)
        self.screen.window.blit(label, (160, 10))
        print(message)

    def _print_replay_message(self) -> None:
        """
        funcion to print the message asking
        if the player wants to play again
        """
        # Clear the top of the screen
        color = self.color.black
        pygame.draw.rect(self.screen.window,
                         color,
                         (0, 0, self.screen.window_width,
                          self.screen.square_size))

        font = pygame.font.SysFont("monospace", 22)
        message: str = "Click anywhere to play again, or press Esc to quit."
        color = self.color.lightblue
        label = font.render(message, 1, color)
        self.screen.window.blit(label, (20, 5))

    def _replay(self, event: pygame.event.EventType) -> bool:
        """
        function to determine if the player wishes to play
        again or not. Returns true if so, false if not.
        """
        self._print_replay_message()
        pygame.display.update()

        # Start an event loop to handle mouse click specifically for replay
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True  # Return True immediately on mouse click

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.delay(100)

    def handle_mouse_motion(self, screen: pygame.Surface,
                            event_pos: list[int]) -> None:
        """
        function to handle mouse motion. This function
        manages the hovering piece that moves across
        the top of the screen before the player plays their
        turn.
        """

        # If the mouse is moving, update the location of
        # the hovering piece
        color = self.color.black
        screen.fill(color)
        self.draw.gameboard()
        posx = event_pos[0]
        if self.turn._player_turn == 1:
            # If it's player 1's turn,
            # the circle will be red
            color = self.color.red
            self.draw.draw_circle(color,
                                  (posx,
                                   int(self.draw.screen.square_size/2)))
        else:
            # If it's player 2's turn,
            # the circle will be yellow
            color = self.color.yellow
            self.draw.draw_circle(color,
                                  (posx,
                                   int(self.draw.screen.square_size/2)))

    def handle_mouse_click(self, event_pos: list[float]) -> Optional[int]:
        """
        function to handle mouse clicking. This function handles
        the response to the player selecting a column to
        place their piece in.
        """

        # If a player has placed a piece...

        # Clear the top of the screen
        color = self.color.black
        pygame.draw.rect(self.screen.window,
                         color,
                         (0, 0, self.screen.window_width,
                          self.screen.square_size))
        try:
            posx = event_pos[0]
            column = int(math.floor(posx/self.screen.square_size))
            # Drop a piece that matches the color of the player
            self.board.drop_piece(column, self.turn._player_turn)

            # Update the state of the board
            self.draw.gameboard()
            pygame.display.update()
            self.turn._increment_turn()
            if (self.board.has_won(self.turn._player_turn)):
                # Check for the winning condition
                self._print_winner_message(self.turn._player_turn)
                return pygame.time.get_ticks()
            elif self.turn._turn_count == 42:
                # Tie game
                self._print_tie_message()
                return pygame.time.get_ticks()
            else:
                self.turn._switch_player()
        except ValueError:
            print("Please enter a valid column on the game board.")
        except FullError:
            print("That column is already full!")
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None
        return None

    def game_loop(self) -> None:
        """
        function to run the game loop.
        """
        pygame.init()
        screen = self.screen.window
        self.draw.gameboard()
        pygame.display.update()
        clock = pygame.time.Clock()
        game_over = False
        wait_time = None

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION and not wait_time:
                    self.handle_mouse_motion(screen, event.pos)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and not wait_time:
                    wait_time = self.handle_mouse_click(event.pos)

            if wait_time:
                # If the game has been won, check how long it's been
                if pygame.time.get_ticks() - wait_time > 3000:
                    # If 3 seconds have passed, end the game
                    # and ask if the player wants to replay

                    replay = self._replay(event)

                    # if response is false, close the game
                    if replay is False:
                        game_over = True
                    else:
                        self.board.reset()  # Reset the board
                        self.draw.gameboard()  # Redraw the empty board

                        game_over = True  # Calling recursively, should end

                        # reset turn variables
                        self.turn._turn_count = 0
                        self.turn._player_turn = 1

                        # start a new game
                        self.game_loop()
                else:
                    pygame.display.update()

            clock.tick(60)  # Keep the game loop running smoothly
