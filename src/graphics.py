import pygame

class Screen():
    def __init__(self, rows: int, cols: int) -> None:
        """
        Constructor for 'Screen'.
        """
        self.square_size = 100
        self.window_width = cols * self.square_size
        self.window_height = (rows+1) * self.square_size
        self.window_size = (self.window_width, self.window_height)
        self.window = pygame.display.set_mode(self.window_size)

class Color():
    def __init__(self) -> None:
        """
        Constructor for 'Color'.
        """
        self.blue = (0,0,255)
        self.black = (0,0,0)

class Draw(Screen):
    def __init__(self, rows: int, cols: int) -> None:
        """
        Constructor for 'Draw'.
        """
        super().__init__(rows, cols)
        self.color = Color()
        self.rows = rows
        self.cols = cols
        self.radius = int(self.square_size/2 - 5)

    def gameboard(self, screen):
        for c in range(self.cols):
            for r in range(self.rows):
                pygame.draw.rect(screen, self.color.blue, 
                                 (c*self.square_size, 
                                  r*self.square_size+self.square_size, 
                                  self.square_size, self.square_size))
                pygame.draw.circle(screen, self.color.black, 
                                   (int(c*self.square_size+self.square_size/2), 
                                    int(r*self.square_size+self.square_size+self.square_size/2)),
                                    self.radius)
