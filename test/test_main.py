import unittest

import main


class TestMain(unittest.TestCase):

    def test_main(self):
        self.assertEqual(main.main(), 'hi')
