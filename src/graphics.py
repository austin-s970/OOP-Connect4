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

    def gameboard(self, screen):
        for c in range(self.board.width):
            for r in range(self.board.height):
                draw_height = self.board.height - r
                pygame.draw.rect(screen, self.color.blue, (c * self.square_size, draw_height * self.square_size, self.square_size, self.square_size))
                occupant = self.board.get_player_at_spot(c, r)
                circle_center = (int(c * self.square_size + self.square_size / 2), int(draw_height * self.square_size + self.square_size / 2))
                if occupant == 1:
                    pygame.draw.circle(screen, self.color.red, circle_center, self.radius)
                elif occupant == 2:
                    pygame.draw.circle(screen, self.color.yellow, circle_center, self.radius)
                else:
                    pygame.draw.circle(screen, self.color.black, circle_center, self.radius)

        pygame.display.update()