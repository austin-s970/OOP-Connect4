"""
Module to handle the input and player turns
"""

import pygame
import sys
import math
from graphics import Color, Draw
from board import Screen, Board, FullError

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
        self.draw: Draw = Draw(self.board)

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

    def _print_winner_message(self, player: int) -> None:
        """
        function to print the message if a player wins
        """
        winner_message = "Congratulations Player " + str(player) + "! You have won the game!"
        print(winner_message)
        sys.exit()

    def game_loop(self) -> None:
        """
        function to run the game loop
        """
        pygame.init()
        screen = self.screen.window
        self.draw.gameboard()
        pygame.display.update()
        clock = pygame.time.Clock()
        # column: int
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    screen.fill(self.color.black)
                    self.draw.gameboard()
                    posx = event.pos[0]
                    if self._player_turn == 1:
                        self.draw.draw_circle(self.color.red,
                                              (posx,
                                               self.draw.square_size/2))
                    else:
                        self.draw.draw_circle(self.color.yellow,
                                              (posx,
                                               self.draw.square_size/2))
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                        posx = event.pos[0]
                        column = int(math.floor(posx/self.screen.square_size))
                        self.board.drop_piece(column, self._player_turn)
                        print(self.board)
                        self.draw.gameboard()
                        pygame.display.update()
                        if (self.board.has_won(self._player_turn)):
                            self._print_winner_message(self._player_turn)
                            game_over = True
                        else:
                            self._switch_player()
                        break
                    except ValueError:
                        print("Please enter a valid column on the game board.")
                    except FullError:
                        print("That column is already full!")
                    except EOFError:
                        return
                    except KeyboardInterrupt:
                        return

        pygame.quit()
