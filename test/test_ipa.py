import unittest
from phonepiece.ipa import read_ipa


class TestIPA(unittest.TestCase):

    def test_all(self):
        ipa = read_ipa()

        # normalize
        self.assertEqual(ipa.normalize('a') , 'a')
        self.assertEqual(ipa.normalize('a:') , 'aː')
        self.assertEqual(ipa.normalize('b') , 'b')
        self.assertEqual(ipa.normalize('g') , 'q')
        self.assertEqual(ipa.normalize('d̠') , 'd')

        # score
        self.assertEqual(ipa.similarity('a', 'a') , 1.0)
        self.assertEqual(ipa.similarity('g', 'q̠') , 1.0)
        self.assertTrue(ipa.similarity('a', 'e') > ipa.similarity('a', 'b'))
        self.assertTrue(ipa.similarity('a', 'ɑ') > ipa.similarity('a', 'i'))
        self.assertTrue(ipa.similarity('a', 'ɑ') > ipa.similarity('ɑ', 'i'))

        # most similar
        self.assertEqual(ipa.most_similar('a', ['b', 's', 'r', 'e']) , 'e')
        self.assertEqual(ipa.most_similar('b', ['p', 's', 'a', 'e']) , 'p')
        self.assertEqual(ipa.most_similar('b', ['b', 's', 'a', 'e']) , 'b')

        self.assertEqual(ipa.tokenize('kʰæt'), ['kʰ', 'æ', 't'])
        self.assertEqual(ipa.tokenize('kʰæ t'), ['kʰ', 'æ', 't'])
        self.assertEqual(ipa.tokenize('a') , ['a'])
        self.assertEqual(ipa.tokenize('aa') , ['a', 'a'])
        self.assertEqual(ipa.tokenize('ab') , ['a', 'b'])
        self.assertEqual(ipa.tokenize('a  a') , ['a', 'a'])

        # remove tones symbols
        self.assertEqual(ipa.tokenize('ʔɓaːn˧˧') , ['ʔ', 'ɓ', 'aː', 'n'])

        # normalizing into the base forms
        self.assertEqual(ipa.compute_base_phone('a'), 'a')
        self.assertEqual(ipa.compute_base_phone('tː'), 't')

