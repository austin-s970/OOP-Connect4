#!/usr/bin/env python3

from board import Board


def draw(board: Board) -> None:
    # draw background
    for x in range(8):
        for y in range(8):
            player_number = board.get_player_at_spot(x, y)
            player_number
            # draw a circle of the correct color at the relavent location


def main() -> None:
    board: Board = Board()
    draw(board)


if __name__ == '__main__':
    main()
