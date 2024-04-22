"""
Module to manage the graphics.
"""

import pygame
from board import Screen, Board, Spot


class Color():
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
    
class Shape(Screen):
    def __init__(self, board: Board) -> None:
        """
        Constructor for 'Shape'.
        """
        super().__init__(board.height, board.width)
        self._spot = Spot()
        self._color = Color()
        self._radius = int(self.square_size/2 - 5)

    @property
    def radius(self) -> int:
        """
        getter property for the radius

        Returns:
            int: the integer representing the radius.
        """
        return self._radius

    def rectangle(self,
                  draw_height: int,
                  draw_width: int,
                  color: tuple[int, int, int]) -> None:
        """
        Given height, width, and a color, draw a rectangle.
        """
        pygame.draw.rect(self.window, color,
                         (draw_width * self.square_size, draw_height *
                          self.square_size, self.square_size,
                          self.square_size))

    def circle(self, color: tuple[int, int, int],
               center: tuple[int, int]) -> None:
        """
        Given a color and a center coordinate, draw a circle.
        """
        pygame.draw.circle(self.window,
                           color, center,
                           self.radius)


class Draw(Screen):
    def __init__(self, board: Board) -> None:
        """
        Constructor for 'Draw'.
        """
        super().__init__(board.height, board.width)
        self._board = board
        self._spot = Spot()
        self._color = Color()
        self._shape = Shape(board)

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
    def shape(self) -> Shape:
        """
        getter property for shapes

        Returns:
            Shape: an instance of the 'Shape' class.
        """
        return self._shape

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

        for c in range(gameboard.width):
            for r in range(gameboard.height):

                draw_height = gameboard.height - r

                self.shape.rectangle(draw_height, c, blue)

                occupant = gameboard.get_player_at_spot(c, r)

                center = (int(c * self.square_size +
                              self.square_size / 2),
                          int(draw_height *
                              self.square_size +
                              self.square_size / 2))

                if occupant == 1:
                    self.shape.circle(red, center)
                elif occupant == 2:
                    self.shape.circle(yellow, center)
                else:
                    self.shape.circle(black, center)

        pygame.display.update()
