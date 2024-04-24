"""
Module to test the Interface class from interface.py     
"""

import unittest
from unittest.mock import Mock, patch
from hypothesis import given, settings, strategies, assume

from turns import Turns


class TestTurns(unittest.TestCase):
    def setUp(self):
        self.turns: Turns = Turns()

    def test_constructor(self) -> None:
        """
        function to test the constructor
        """
        test_inter: Turns = Turns()
        self.assertEqual(test_inter.player_turn, 1)
        self.assertEqual(test_inter.turn_count, 0)