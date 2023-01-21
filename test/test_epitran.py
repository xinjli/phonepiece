import unittest
from phonepiece.epitran import read_epitran_g2p
from phonepiece.inventory import read_inventory

class TestEpitran(unittest.TestCase):

    def test_all(self):
        epi = read_epitran_g2p('spa')
        self.assertTrue(epi['b'] == ['b'])

    def test_g2p_in_phoneme(self):

        langs = ['spa', 'deu', 'fra', 'ita', 'rus', 'tur']

        for lang_id in langs:
            epi = read_epitran_g2p(lang_id)
            inv = read_inventory(lang_id)

            for vs in epi.values():
                for v in vs:
                    self.assertTrue(v in inv.phoneme)