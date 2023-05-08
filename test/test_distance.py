import unittest
from phonepiece.distance import phonological_distance

class TestDistance(unittest.TestCase):

    def test_all(self):

        self.assertEqual(phonological_distance('a', 'a') == 0.0)
        self.assertEqual(phonological_distance('a', 'a') == 1.0)