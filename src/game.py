"""
    Module for the game
"""
from typing import Optional

import pygame
import sys
import math

from interface import Interface
from board import Board, Screen, FullError
from graphics import Color, Draw


class Game():
    """
    Mediator class for the game
    """
    def __init__(self) -> None:
        """
        constructor
        """
        self.inter: Interface = Interface()
        self.board: Board = Board()
        self.screen: Screen = Screen(self.board.height, self.board.width)
        self.color: Color = Color()
        self.draw: Draw = Draw(self.board)

    def _print_winner_message(self, player: int) -> None:
        """
        function to print the message if a player wins.
        """
        font = pygame.font.SysFont("monospace", 75)
        message: str = "Player " + str(player) + " wins!"
        if player == 1:
            label = font.render(message, 1, self.color.red)
            self.screen.window.blit(label, (40, 10))
        else:
            label = font.render(message, 1, self.color.yellow)
            self.screen.window.blit(label, (40, 10))
        print(message)

    def _print_tie_message(self) -> None:
        """
        funcion to print the message if the players tie
        """
        font = pygame.font.SysFont("monospace", 75)
        message: str = "Tie Game!"
        label = font.render(message, 1, self.color.blue)
        self.screen.window.blit(label, (40, 10))
        print(message)

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
                    # If 3 seconds have passed, close the window
                    game_over = True
                else:
                    pygame.display.update()

            clock.tick(60)  # Keep the game loop running smoothly

        pygame.quit()  # End the game

    def handle_mouse_motion(self, screen: pygame.Surface,
                            event_pos: list[int]) -> None:
        # If the mouse is moving, update the location of
        # the hovering piece
        screen.fill(self.color.black)
        self.draw.gameboard()
        posx = event_pos[0]
        if self.inter._player_turn == 1:
            # If it's player 1's turn,
            # the circle will be red
            self.draw.draw_circle(self.color.red,
                                  (posx,
                                   int(self.draw.square_size/2)))
        else:
            # If it's player 2's turn,
            # the circle will be yellow
            self.draw.draw_circle(self.color.yellow,
                                  (posx,
                                   int(self.draw.square_size/2)))

    def handle_mouse_click(self, event_pos: list[float]) -> Optional[int]:
        # If a player has placed a piece...

        # Clear the top of the screen
        pygame.draw.rect(self.screen.window,
                         self.color.black,
                         (0, 0, self.screen.window_width,
                          self.screen.square_size))
        try:
            posx = event_pos[0]
            column = int(math.floor(posx/self.screen.square_size))
            # Drop a piece that matches the color of the player
            self.board.drop_piece(column, self.inter._player_turn)

            # Update the state of the board
            self.draw.gameboard()
            pygame.display.update()
            self.inter._increment_turn()
            if (self.board.has_won(self.inter._player_turn)):
                # Check for the winning condition
                self._print_winner_message(self.inter._player_turn)
                return pygame.time.get_ticks()
            elif self.inter._turn_count == 42:
                # Tie game
                self._print_tie_message()
                return pygame.time.get_ticks()
            else:
                self.inter._switch_player()
        except ValueError:
            print("Please enter a valid column on the game board.")
        except FullError:
            print("That column is already full!")
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None
        return None
