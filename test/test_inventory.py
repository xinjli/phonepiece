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

    def test_allophone(self):

        target_langs = ['eng', 'cmn', 'jpn', 'deu', 'spa', 'fra', 'rus', 'tur', 'ita']

        for lang_id in target_langs:
            inv = read_inventory(lang_id)

            for phone in inv.phone2phoneme.keys():
                self.assertTrue(phone in inv.phone)

            for phoneme in inv.phoneme2phone.keys():
                self.assertTrue(phone in inv.phoneme)