"""
Module to manage the graphics.
"""

import pygame
from board import Screen, Board, Spot


class Color():
    def get_color(self) -> tuple[int, int, int]:
        raise NotImplementedError


class Red(Color):
    def get_color(self) -> tuple[int, int , int]:
        """
        getter property for the color 'red'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        red = (255, 0, 0)
        return red


class Blue(Color):
    def get_color(self) -> tuple[int, int , int]:
        """
        getter property for the color 'blue'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        blue = (0, 0, 255)
        return blue


class Yellow(Color):
    def get_color(self) -> tuple[int, int , int]:
        """
        getter property for the color 'yellow'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        yellow = (255, 255, 0)
        return yellow


class Black(Color):
    def get_color(self) -> tuple[int, int , int]:
        """
        getter property for the color 'black'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        black = (0, 0, 0)
        return black


class LightBlue(Color):
    def get_color(self) -> tuple[int, int , int]:
        """
        getter property for the color 'lightblue'

        Returns:
            tuple[int, int, int]: a tuple representing the RGB value.
        """
        lightblue = (0, 255, 255)
        return lightblue


class Shape(Screen):
    def __init__(self, color: Color, board: Board) -> None:
        """
        Constructor for 'Shape'.
        """
        super().__init__(board.rows, board.cols)
        self._color = color
        self._board = board
        self._radius = int(self.square_size/2 - 5)

    @property
    def radius(self) -> int:
        """
        getter property for the radius

        Returns:
            int: the integer representing the radius.
        """
        return self._radius

    def draw(self, window):
        raise NotImplementedError("This method should be overridden by subclasses")


class Rectangle(Shape):
    def __init__(self, color: Color, board: Board):
        super().__init__(color, board)

    def draw(self, window, draw_height: int, draw_width: int):
        """
        Draw a rectangle at the given position with the color of this shape.
        """
        color = self._color.get_color()  # Use get_color from the color instance
        pygame.draw.rect(window, color,
                         (draw_width * self.square_size, draw_height * self.square_size,
                          self.square_size, self.square_size))


class Circle(Shape):
    def __init__(self, color: Color, board: Board):
        super().__init__(color, board)

    def draw(self, window, center: tuple[int, int]):
        """
        Draw a circle at the given center with the color of this shape.
        """
        color = self._color.get_color()  # Use get_color from the color instance
        pygame.draw.circle(window, color, center, self.radius)


class Draw(Screen):
    def __init__(self, board: Board) -> None:
        """
        Constructor for 'Draw'.
        """
        super().__init__(board.height, board.width)
        self._board = board
        self._red = Red()
        self._blue = Blue()
        self._yellow = Yellow()
        self._black = Black()

    @property
    def board(self) -> Board:
        """
        getter property for the board

        Returns:
            Board: an instance of the 'Board' class.
        """
        return self._board

    @property
    def red(self) -> Red:
        """
        getter property for the color 'Red'

        Returns:
            Red: an instance of the 'Red' subclass.
        """
        return self._red

    @property
    def blue(self) -> Blue:
        """
        getter property for the color 'Blue'

        Returns:
            Blue: an instance of the 'Blue' subclass.
        """
        return self._blue

    @property
    def yellow(self) -> Yellow:
        """
        getter property for the color 'Yellow'

        Returns:
            Yellow: an instance of the 'Yellow' subclass.
        """
        return self._yellow
    
    @property
    def black(self) -> Black:
        """
        getter property for the color 'Black'

        Returns:
            Black: an instance of the 'Black' subclass.
        """
        return self._black

    def gameboard(self) -> None:
        """
        Draw the current graphical representation
        of the board.
        """
        # Define the colors to be used for the board
        # and pieces.

        gameboard = self.board

        for c in range(gameboard.width):
            for r in range(gameboard.height):

                draw_height = gameboard.height - r

                rectangle = Rectangle(self.blue, gameboard)
                rectangle.draw(self.window, draw_height, c)

                occupant = gameboard.get_player_at_spot(c, r)

                center = (int(c * self.square_size +
                              self.square_size / 2),
                          int(draw_height *
                              self.square_size +
                              self.square_size / 2))

                if occupant == 1:
                    circle = Circle(self.red, gameboard)
                    circle.draw(self.window, center)
                elif occupant == 2:
                    circle = Circle(self.yellow, gameboard)
                    circle.draw(self.window, center)  
                else:
                    circle = Circle(self.black, gameboard)
                    circle.draw(self.window, center)

        pygame.display.update()
