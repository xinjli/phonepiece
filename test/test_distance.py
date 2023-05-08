import unittest
from phonepiece.distance import phonological_distance, edit_distance

class TestDistance(unittest.TestCase):

    def test_all(self):

        self.assertEqual(edit_distance('a', 'a')[0], 0)
        self.assertEqual(edit_distance('a', 'b')[0], 1)
        self.assertEqual(phonological_distance('a', 'a'), 0)