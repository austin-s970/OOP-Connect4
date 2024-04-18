"""
Module to handle the input and player turns
"""

import pygame
import sys
from graphics import Screen, Color, Draw
from board import Board, FullError

class Interface():

    def __init__(self) -> None:
        """
        constructor
        """
        self._player_turn: int = 1
        self._turn_count: int = 0
        self.board: Board = Board()
        self.screen: Screen = Screen(self.board.height, self.board.width)
        self.color: Color = Color()
        self.draw: Draw = Draw(self.board.height, self.board.width)

    def print_welcome(self) -> None:
        """
        function to print the welcome message for the game
        """
        pass

    def _print_turn_instructions(self) -> None:
        """
        function to print the turn instructions for the players
        """
        print(f"""Its Player {self._player_turn}'s turn!
              Please enter the column number to drop a piece.""")

    def _switch_player(self) -> None:
        """
        function to switch the player turn
        """
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    @property
    def player_turn(self) -> int:
        """
        getter property for the player_turn

        Returns:
            int: the integer representing what player's turn it is
        """
        return self._player_turn

    def _read_input(self) -> int:
        """
        function to read the input from the players

        Returns:
            int: the column that the player specified
        """
        column: int
        line: str = input()
        while True:
            try:
                column = int(line)
                break
            except ValueError:
                print("Please enter a valid column number.")
        return column

    def _print_winner_message(self) -> None:
        """
        function to print the message if a player wins
        """
        pass

    def game_loop(self) -> None:
        """
        function to run the game loop
        """
        pygame.init()
        screen = self.screen.window
        self.draw.gameboard(screen)
        pygame.display.update()
        clock = pygame.time.Clock()
        # column: int
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse button down
                    pass
            self.draw.gameboard(screen)
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
