"""
Module to handle the input and player turns.
"""


class Interface():
    def __init__(self) -> None:
        """
        constructor.
        """
        self._player_turn: int = 1
        self._turn_count: int = 0

    def print_welcome(self) -> None:
        """
        function to print the welcome message for the game.
        """
        pass

    def _print_turn_instructions(self) -> None:
        """
        function to print the turn instructions for the players.
        """
        print(f"""Its Player {self._player_turn}'s turn!
              Please enter the column number to drop a piece.""")

    def _switch_player(self) -> None:
        """
        function to switch the player turn.
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
            int: the integer representing what player's turn it is.
        """
        return self._player_turn

    @property
    def turn_count(self) -> int:
        """
        getter property for the turn count

        Returns:
            int: the integer the turn count.
        """
        return self._turn_count

    def _increment_turn(self) -> None:
        """
        function to increment the game turn
        """
        self._turn_count += 1
