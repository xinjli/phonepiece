import unittest
from phonepiece.lexicon import read_lexicon


class TestLexicon(unittest.TestCase):

    def test_all(self):


        rus = read_lexicon('rus')
        assert rus['язык'] == ['j', 'i', 'z', 'ɨ', 'k']