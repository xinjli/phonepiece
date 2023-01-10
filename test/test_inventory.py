import unittest
from phonepiece.inventory import read_inventory


class TestInventory(unittest.TestCase):

    def test_all(self):
        inv = read_inventory('eng')

        phones = inv.phone.tolist()
        self.assertTrue(phones[0] == '<blk>')
        self.assertTrue(phones[-1] == '<eos>')

        phonemes = inv.phoneme.tolist()
        self.assertTrue(phonemes[0] == '<blk>')
        self.assertTrue(phonemes[-1] == '<eos>')