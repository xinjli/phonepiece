# -*- coding: utf-8 -*-
# this file is adapted from epitran

import csv
from phonepiece.config import PhonePieceConfig
from phonepiece.ipa import read_ipa

def none2str(x):
    return x if x else ''


class ArpaConverter:

    def __init__(self):
        arpa_path = PhonePieceConfig.data_path / 'arpabet.csv'

        self.ipa = read_ipa()

        self.arpa_map = {}
        self.ipa_to_arpa = {}

        self.ipa_set = set()

        with open(arpa_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for arpa, ipa in reader:
                ipa = ipa.strip()
                self.arpa_map[arpa] = ipa.split()

                # only register 1 ipa 1 arpa mapping
                if len(ipa.split()) > 1:
                    continue

                self.ipa_to_arpa[ipa] = arpa

                self.ipa_set.update(ipa.split())

    def convert(self, str_or_lst):
        if isinstance(str_or_lst, str):
            str_or_lst = str_or_lst.split(' ')

        result = []
        for arpa in str_or_lst:
            if str.isdigit(arpa[-1]):
                arpa = arpa[:-1]

            result.extend(self.arpa_map[arpa.lower()])

        return result

    def convert_ipa_to_arpa(self, ipa_lst):

        normalized_ipa = []
        for ipa in ipa_lst:
            normalized_ipa.append(self.ipa.most_similar(ipa, sorted(list(self.ipa_set))))

        arpa_lst = []

        while len(normalized_ipa) > 0:
            two_ipa_arpa = " ".join(normalized_ipa[:2])
            if two_ipa_arpa in self.ipa_to_arpa:
                arpa_lst.append(self.ipa_to_arpa[two_ipa_arpa])
                normalized_ipa = normalized_ipa[2:]
                continue

            ipa = normalized_ipa[0]
            if ipa in self.ipa_to_arpa:
                arpa_lst.append(self.ipa_to_arpa[ipa])

            normalized_ipa = normalized_ipa[1:]

        return arpa_lst