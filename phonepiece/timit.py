import csv
from phonepiece.config import PhonePieceConfig
from phonepiece.arpa import ArpaConverter


class TIMITConverter:

    def __init__(self):

        timit_path = PhonePieceConfig.data_path / 'timit.txt'

        self.timit_map = {}

        with open(timit_path, 'r') as f:
            for line in f:
                fields = line.strip().split()

                if fields[1] != 'nan':
                    self.timit_map[fields[0]] = fields[2]
                else:
                    self.timit_map[fields[0]] = ''

        self.arpa_converter = ArpaConverter()

        self.cache = {}

    def convert(self, str_or_lst):

        if isinstance(str_or_lst, str):
            str_or_lst = str_or_lst.split(' ')

        result = []
        for phone in str_or_lst:
            phone = phone.lower()

            if phone in self.cache:
                result.extend(self.cache[phone])
                continue

            if phone not in self.timit_map:
                PhonePieceConfig.logger.error(f"{phone} is not a TIMIT phone")

            timit_phone = self.timit_map[phone]

            # skip q and silence
            if timit_phone == '' or timit_phone == 'sil':
                continue

            ipa_phone = self.arpa_converter.convert(timit_phone)
            self.cache[phone] = ipa_phone

            result.extend(ipa_phone)

        return result