#!/usr/bin/env python3

from board import Board
from interface import Interface


def draw(board: Board) -> None:
    # draw background
    for x in range(7):
        for y in range(6):
            # player_number = board.get_player_at_spot(x, y)
            # draw a circle of the correct color at the relavent location
            pass


def main() -> None:
    game_interface = Interface()  # Initialize the game interface
    game_interface.print_welcome()  # Optionally, print a welcome message
    game_interface.game_loop()  # Start the game loop
    # board: Board = Board()
    # draw(board)


if __name__ == '__main__':
    main()
