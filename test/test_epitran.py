import unittest
from phonepiece.epitran import read_epitran_g2p


class TestEpitran(unittest.TestCase):

    def test_all(self):
        epi = read_epitran_g2p('spa')
        self.assertTrue(epi['b'] == ['b'])