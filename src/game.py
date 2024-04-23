"""
Module containing the Game Mediator Class
"""

from typing import Optional

import pygame
import sys
import math

from graphics import Color, Shape, Draw
from graphics import Red, Blue, Yellow, Black, LightBlue
from graphics import Rectangle, Circle
from board import Screen, Board, FullError
from interface import Interface


class Game():
    """
    Game mediator class
    """
    def __init__(self) -> None:
        """
        constructor
        """
        self.inter: Interface = Interface()
        self._board: Board = Board()
        self._screen: Screen = Screen(self._board.height, self._board.width)
        self._red: Red = Red()
        self._blue: Blue = Blue()
        self._yellow: Yellow = Yellow()
        self._black: Black = Black()
        self._lightblue: LightBlue = LightBlue()
        self._draw: Draw = Draw(self._board)

    @property
    def screen(self) -> Screen:
        """
        getter property for the screen

        Returns:
            Screen: an instance of the 'Screen' class.
        """
        return self._screen

    @property
    def board(self) -> Board:
        """
        getter property for the board

        Returns:
            Board: an instance of the 'Board' class.
        """
        return self._board

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
            color = self._red.get_color()
            label = font.render(message, 1, color)
            self.screen.window.blit(label, (40, 10))
        else:
            color = self._yellow.get_color()
            label = font.render(message, 1, color)
            self.screen.window.blit(label, (40, 10))
        print(message)

    def _print_tie_message(self) -> None:
        """
        funcion to print the message if the players tie
        """
        font = pygame.font.SysFont("monospace", 75)
        message: str = "Tie Game!"
        color = self._blue.get_color()
        label = font.render(message, 1, color)
        self.screen.window.blit(label, (160, 10))
        print(message)

    def _print_replay_message(self) -> None:
        """
        funcion to print the message asking
        if the player wants to play again
        """
        # Clear the top of the screen
        color = self._black.get_color()
        pygame.draw.rect(self.screen.window,
                         color,
                         (0, 0, self.screen.window_width,
                          self.screen.square_size))

        font = pygame.font.SysFont("monospace", 22)
        message: str = "Click anywhere to play again, or press Esc to quit."
        color = self._lightblue.get_color()
        label = font.render(message, 1, color)
        self.screen.window.blit(label, (20, 5))

    def _end_game(self, event: pygame.event.EventType) -> bool:
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
                    self.reset_game()
                    return False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
    def reset_game(self) -> None:
        """
        Resets the game board and relevant game state variables to start a new game.
        """
        self.board.reset()  # Reset the board to an empty state
        self.inter._turn_count = 0  # Reset the turn count
        self.inter._player_turn = 1  # Start with player 1
        self.draw.gameboard()  # Redraw the empty board for a new game
        pygame.display.update()  # Update the display to show the reset board

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

            pygame.display.update()
            clock.tick(60)  # Keep the game loop running smoothly

            game_over = self._end_game()

    def handle_mouse_motion(self, screen: pygame.Surface,
                            event_pos: list[int]) -> None:
        # If the mouse is moving, update the location of
        # the hovering piece
        rect = pygame.Rect(0, 0, self.screen.window_width, self.screen.square_size)
        screen.fill(self._black.get_color(), rect)
        self.draw.gameboard()
        posx = event_pos[0]
        center = (posx, int(self.screen.square_size / 2))

        if self.inter._player_turn == 1:
            # If it's player 1's turn,
            # the circle will be red
            circle = Circle(self.draw.red, self.board)
        else:
            # If it's player 2's turn,
            # the circle will be yellow
            circle = Circle(self.draw.yellow, self.board)
        circle.draw(self.screen.window, center)

    def handle_mouse_click(self, event_pos: list[float]) -> None:
        # Try to place a piece and redraw only if successful
        posx = event_pos[0]
        column = int(math.floor(posx/self.screen.square_size))
        try:
            if self.board.drop_piece(column, self.inter._player_turn):  # Ensure drop_piece returns a boolean
                self.inter._increment_turn()
                self.draw.gameboard()  # Draw new board state
                if self.board.has_won(self.inter._player_turn):
                    self._print_winner_message(self.inter._player_turn)
                    pygame.time.wait(3000)  # Delay to show message
                elif self.inter._turn_count == 42:
                    self._print_tie_message()
                    pygame.time.wait(3000)
        except FullError:
            print("That column is already full!")
        except KeyboardInterrupt:
            return None
        return None