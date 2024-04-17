#!/usr/bin/env python3

from interface import Interface


def main() -> None:
    interface: Interface = Interface()
    interface.game_loop()


if __name__ == '__main__':
    main()
