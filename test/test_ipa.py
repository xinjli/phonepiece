import unittest
from phonepiece.ipa import read_ipa


class TestIPA(unittest.TestCase):

    def test_all(self):
        ipa = read_ipa()

        # normalize
        self.assertTrue(ipa.normalize('a') == 'a')
        self.assertTrue(ipa.normalize('a:') == 'aː')
        self.assertTrue(ipa.normalize('b') == 'b')
        self.assertTrue(ipa.normalize('g') == 'q')
        self.assertTrue(ipa.normalize('d̠') == 'd')

        # score
        self.assertTrue(ipa.similarity('a', 'a') == 1.0)
        self.assertTrue(ipa.similarity('g', 'q̠') == 1.0)
        self.assertTrue(ipa.similarity('a', 'e') > ipa.similarity('a', 'b'))
        self.assertTrue(ipa.similarity('a', 'ɑ') > ipa.similarity('a', 'i'))
        self.assertTrue(ipa.similarity('a', 'ɑ') > ipa.similarity('ɑ', 'i'))

        # most similar
        self.assertTrue(ipa.most_similar('a', ['b', 's', 'r', 'e']) == 'e')
        self.assertTrue(ipa.most_similar('b', ['p', 's', 'a', 'e']) == 'p')
        self.assertTrue(ipa.most_similar('b', ['b', 's', 'a', 'e']) == 'b')

        self.assertTrue(ipa.tokenize('kʰæt') == ['kʰ', 'æ', 't'])
        self.assertTrue(ipa.tokenize('kʰæ t') == ['kʰ', 'æ', 't'])
        self.assertTrue(ipa.tokenize('a') == ['a'])
        self.assertTrue(ipa.tokenize('aa') == ['a', 'a'])
        self.assertTrue(ipa.tokenize('ab') == ['a', 'b'])
        self.assertTrue(ipa.tokenize('a  a') == ['a', 'a'])

