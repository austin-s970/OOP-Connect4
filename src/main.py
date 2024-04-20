#!/usr/bin/env python3

from game import Game


def main() -> None:
    game: Game = Game()
    game.game_loop()


if __name__ == '__main__':
    main()
