import pygame
from board import Screen, Board, Spot, Piece

class Color():
    def __init__(self) -> None:
        """
        Constructor for 'Color'.
        """
        self.red = (255,0,0)
        self.blue = (0,0,255)
        self.yellow = (255,255,0)
        self.black = (0,0,0)

class Draw(Screen):
    def __init__(self, board: Board) -> None:
        """
        Constructor for 'Draw'.
        """
        super().__init__(board.height, board.width)
        self.board = board
        self.spot = Spot()
        self.piece = Piece(None)
        self.color = Color()
        self.radius = int(self.square_size/2 - 5)
    
    def draw_rectangle(self, draw_height: int,
                       draw_width: int,
                       color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.window, color,
                         (draw_width * self.square_size, draw_height *
                          self.square_size, self.square_size,
                          self.square_size))
        
    def draw_circle(self, color: tuple[int, int, int],
                    center: tuple[int, int]) -> None:
        pygame.draw.circle(self.window,
                           color, center,
                           self.radius)

    def gameboard(self):
        for c in range(self.board.width):
            for r in range(self.board.height):

                draw_height = self.board.height - r

                self.draw_rectangle(draw_height, c, self.color.blue)

                occupant = self.board.get_player_at_spot(c, r)

                center = (int(c * self.square_size +
                              self.square_size / 2),
                              int(draw_height *
                                  self.square_size +
                                  self.square_size / 2))

                if occupant == 1:
                    self.draw_circle(self.color.red, center)
                elif occupant == 2:
                    self.draw_circle(self.color.yellow, center)
                else:
                    self.draw_circle(self.color.black, center)

        pygame.display.update()