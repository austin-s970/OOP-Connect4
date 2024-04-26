"""
Module to test the Interface class from interface.py     
"""

import unittest
from unittest.mock import Mock, patch
from hypothesis import given, settings, strategies, assume
import hypothesis.strategies as some

from turns import Turns


class TestTurns(unittest.TestCase):
    def setUp(self):
        """
        Setup function for 'TestTurns'.
        This function initializes
        an instance of 'Turns' to do
        tests on.
        """
        self.turns: Turns = Turns()

    def test_constructor(self) -> None:
        """
        function to test the constructor
        """
        test_inter: Turns = Turns()
        self.assertEqual(test_inter.player_turn, 1)
        self.assertEqual(test_inter.turn_count, 0)

    @given(some.integers(min_value=1, max_value=2))
    def test_switch_player(self, test_int: int) -> None:
        """
        function to test the switch player function
        """
        self.turns._player_turn = test_int
        if test_int == 1:
            self.turns._switch_player()
            self.assertEqual(self.turns._player_turn, 2)
        elif test_int == 2:
            self.turns._switch_player()
            self.assertEqual(self.turns._player_turn, 1)

    @given(some.integers())
    def test_player_turn_getter(self, test_int: int) -> None:
        """
        function to test the player_turn getter property
        """
        self.turns._player_turn = test_int
        self.assertEqual(self.turns.player_turn, test_int)

    @given(some.integers())
    def test_turn_count(self, test_int: int) -> None:
        """
        function to test the turn_count getter property
        """
        self.turns._turn_count = test_int
        self.assertEqual(self.turns._turn_count, test_int)

    @given(some.integers())
    def test_increment_turn(self, test_int: int) -> None:
        """
        function to test the increment_turn function
        """
        self.turns._turn_count = test_int
        self.turns._increment_turn()
        self.assertEqual(self.turns._turn_count, test_int + 1)