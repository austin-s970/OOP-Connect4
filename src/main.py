#!/usr/bin/env python3
"""
Main module.
"""

from game import Game


def main() -> None:
    """
    Main function. When called,
    this function runs the game
    application.
    """
    game: Game = Game()
    game.game_loop()


if __name__ == '__main__':
    main()
