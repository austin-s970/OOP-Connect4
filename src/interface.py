"""
Module to handle the input and player turns
"""

from board import Board, FullError


class Interface():

    def __init__(self) -> None:
        """
        constructor
        """
        self._player_turn: int = 1
        self._turn_count: int = 0
        self.board: Board = Board()

    def print_welcome(self) -> None:
        """
        function to print the welcome message for the game
        """
        pass

    def _print_turn_instructions(self) -> None:
        """
        function to print the turn instructions for the players
        """
        print(f"""Its Player {self._player_turn}'s turn!
              Please enter the column number to drop a piece.""")

    def _switch_player(self) -> None:
        """
        function to switch the player turn
        """
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    @property
    def player_turn(self) -> int:
        """
        getter property for the player_turn

        Returns:
            int: the integer representing what player's turn it is
        """
        return self._player_turn

    def _read_input(self) -> int:
        """
        function to read the input from the players

        Returns:
            int: the column that the player specified
        """
        column: int
        line: str = input()
        while True:
            try:
                column = int(line)
                break
            except ValueError:
                print("Please enter a valid column number.")
        return column

    def _print_winner_message(self) -> None:
        """
        function to print the message if a player wins
        """
        pass

    def game_loop(self) -> None:
        """
        function to run the game loop
        """
        column: int
        while True:
            self._print_turn_instructions()
            while True:
                try:
                    column = self._read_input()
                    self.board.drop_piece(column - 1, self._player_turn)
                    break
                except ValueError:
                    print("Please enter a valid column on the game board.")
                except FullError:
                    print("That column is already full!")
            if (self.board.has_won(self._player_turn)):
                self._print_winner_message()
                break
            else:
                self._switch_player()
