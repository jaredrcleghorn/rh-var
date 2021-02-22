import unittest
import utils

class TestFunctions(unittest.TestCase):
    def test_convert_to_returns(self):
        self.assertEqual(utils.convert_to_returns((1, 2, 3)), (1, 0.5))
