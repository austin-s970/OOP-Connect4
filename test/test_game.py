"""
Module for testing the game mediator class from game.py    
"""

import unittest
from unittest.mock import Mock, patch
from hypothesis import given, settings, strategies, assume
import hypothesis.strategies as some

from game import Game


class TestGame(unittest.TestCase):
    """
    Class for testing Game()
    """
    def setUp(self):
        self.game: Game = Game()

    

