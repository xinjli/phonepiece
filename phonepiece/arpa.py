# -*- coding: utf-8 -*-
# this file is adapted from epitran

import csv
from phonepiece.config import PhonePieceConfig


def none2str(x):
    return x if x else ''


class ArpaConverter:

    def __init__(self):
        arpa_path = PhonePieceConfig.data_path / 'arpabet.csv'

        self.arpa_map = {}
        with open(arpa_path, 'r') as f:
            reader = csv.reader(f)
            for arpa, ipa in reader:
                self.arpa_map[arpa] = ipa.strip().split()

    def convert(self, str_or_lst):
        if isinstance(str_or_lst, str):
            str_or_lst = str_or_lst.split(' ')

        result = []
        for arpa in str_or_lst:
            if str.isdigit(arpa[-1]):
                arpa = arpa[:-1]

            result.extend(self.arpa_map[arpa.lower()])

        return result