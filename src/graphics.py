"""
Module to manage the graphics.
"""

import pygame
from board import Screen, Board, Spot
from typing import Dict, Any


class MultiError(Exception):
    """
    Custom exception to handle
    the case that multiple instances
    of 'Draw' exist.
    """
    pass


class Color():
    """
    Class controlling the colors.
    """
    def __init__(self) -> None:
        """
        Constructor for 'Color'.
        """
        self._red = (255, 0, 0)
        self._blue = (0, 0, 255)
        self._yellow = (255, 255, 0)
        self._lightblue = (0, 255, 255)
        self._black = (0, 0, 0)

    @property
    def red(self) -> tuple[int, int , int]:
        """
        getter property for the color 'red'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        return self._red

    @property
    def blue(self) -> tuple[int, int , int]:
        """
        getter property for the color 'blue'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        return self._blue

    @property
    def yellow(self) -> tuple[int, int , int]:
        """
        getter property for the color 'yellow'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        return self._yellow

    @property
    def lightblue(self) -> tuple[int, int , int]:
        """
        getter property for the color 'lightblue'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        return self._lightblue

    @property
    def black(self) -> tuple[int, int , int]:
        """
        getter property for the color 'black'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        return self._black


class DrawMeta(type):
    """
    Meta-class for 'Draw'. This class
    ensures that no more than one
    instance of 'Draw' exists.
    """

    # Attribute to store the singleton instance:
    _instances: Dict[Any, Any] = {}

    def __call__(cls: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Control the creation of new instances,
        ensuring that no more than one
        instance exists.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Draw(metaclass=DrawMeta):
    """
    Class that draws the graphics of
    the game.
    """
    __initialized: bool = False

    def __init__(self, board: Board) -> None:
        """
        Constructor for 'Draw'.
        """
        if self.__initialized:
            return
        self._screen = Screen(board.height, board.width)
        self._board = board
        self._spot = Spot()
        self._color = Color()
        self._radius = int(self.screen.square_size/2 - 5)

        # set a variable, '__initialized' to True
        # This prevents re-initialization:
        self.__initialized = True

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
    def spot(self) -> Spot:
        """
        getter property for a spot on the board

        Returns:
            Spot: an instance of the 'Spot' class.
        """
        return self._spot

    @property
    def color(self) -> Color:
        """
        getter property for a color

        Returns:
            Color: an instance of the 'Color' class.
        """
        return self._color

    @property
    def radius(self) -> int:
        """
        getter property for the radius

        Returns:
            int: the integer representing the radius.
        """
        return self._radius

    def draw_rectangle(self,
                       draw_height: int,
                       draw_width: int,
                       color: tuple[int, int, int]) -> None:
        """
        Given height, width, and a color, draw a rectangle.
        """
        pygame.draw.rect(self.screen.window, color,
                         (draw_width * self.screen.square_size, draw_height *
                          self.screen.square_size, self.screen.square_size,
                          self.screen.square_size))

    def draw_circle(self, color: tuple[int, int, int],
                    center: tuple[int, int]) -> None:
        """
        Given a color and a center coordinate, draw a circle.
        """
        pygame.draw.circle(self.screen.window,
                           color, center,
                           self.radius)

    def gameboard(self) -> None:
        """
        Draw the current graphical representation
        of the board.
        """
        # Define the colors to be used for the board
        # and pieces.

        hue = self.color

        red = hue.red
        blue = hue.blue
        yellow = hue.yellow
        black = hue.black

        gameboard = self.board

        for r, c, spot in gameboard:
            draw_height = gameboard.height - r

            self.draw_rectangle(draw_height, c, blue)

            occupant = spot.player_number()

            center = (int(c * self.screen.square_size +
                          self.screen.square_size / 2),
                      int(draw_height *
                          self.screen.square_size +
                          self.screen.square_size / 2))
            if occupant == 1:
                self.draw_circle(red, center)
            elif occupant == 2:
                self.draw_circle(yellow, center)
            else:
                self.draw_circle(black, center)

        pygame.display.update()
