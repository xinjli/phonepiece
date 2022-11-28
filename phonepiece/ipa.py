import numpy as np
from phonepiece.config import PhonePieceConfig
import csv
import unicodedata

_norm_rules = [
    (':', 'ː'),
    ("ɡ̥", "k"),
    ('g', 'q̠'),
    ('d̥', "t"),
    ("b̥", "b"),
    ("'", "ʼ"),
]


def read_ipa():

    feature_file = PhonePieceConfig.data_path / f'ipa_all.csv'

    feature_map = {'0': 0, '-': -1, '+': 1}

    phone2feature = {}

    with open(feature_file) as csvfile:
        reader = csv.reader(csvfile)

        # This skips the first row of the CSV file.
        next(reader)

        for row in reader:
            phone = unicodedata.normalize('NFD', row[0])
            features = list(map(lambda x: feature_map[x], row[1:]))
            assert len(features) == 24
            phone2feature[phone] = np.array(features)

    # weights are taken from panphon ipa_weights
    weights = [
       1,1,1,0.5,0.25,0.25,0.25,0.125,0.125,0.125,0.125,0.25,0.25,0.125,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.125,0,0
    ]

    assert len(weights) == 24

    return IPA(phone2feature, weights)


class IPA:

    def __init__(self, phone2feature, weights):
        self.phone2feature = phone2feature
        self.weights = weights

    def __getitem__(self, item):
        item = self.normalize(item)
        if item in self.phone2feature:
            return self.phone2feature[item]
        else:
            return np.zeros(24, dtype=np.int32)

    def __contains__(self, item):
        item = self.normalize(item)
        return item in self.phone2feature

    def normalize(self, orig_phone):
        norm_phone = unicodedata.normalize('NFD', orig_phone)

        # normalize some easy mistakes
        for rule in _norm_rules:
            norm_phone = norm_phone.replace(rule[0], rule[1])

        phone = norm_phone
        # strip diacritics until it find match
        while len(phone) > 0:
            if phone in self.phone2feature:
                return phone
            phone = phone[:-1]

        # guard cases such as: ʰk
        if len(norm_phone) > 1 and norm_phone[1:] in self.phone2feature:
            return norm_phone[1:]

        # guard cases such as ʰkʷ
        if len(norm_phone) > 2 and norm_phone[1:-1] in self.phone2feature:
            return norm_phone[1:-1]

        # give up ... and return [!] as an invalid phone to debug
        PhonePieceConfig.logger.error(f"cannot normalize phone {orig_phone}")
        return '!'

    def tokenize(self, orig_phone):
        norm_phone = unicodedata.normalize('NFD', orig_phone)

        # normalize some easy mistakes
        for rule in _norm_rules:
            norm_phone = norm_phone.replace(rule[0], rule[1])

        phone = norm_phone

        res = []
        i = 0
        while i < len(phone):
            longest_len = -1

            for j in range(1, min(8, len(phone) - i)+1):
                if phone[i:i+j] in self.phone2feature:
                    longest_len = j

            if longest_len != -1:
                subphone = phone[i:i+longest_len]
                res.append(subphone)
                i += len(subphone)
            else:
                i += 1

        return res

    def similarity(self, p1, p2):
        """
        similarity between phone 1 and phone 2

        :param p1:
        :param p2:
        :return:
        """

        p1 = self.normalize(p1)
        p2 = self.normalize(p2)

        # similarity is 0 if either entry is not found
        if p1 not in self.phone2feature or p2 not in self.phone2feature:
            return 0

        f1 = self.phone2feature[p1]
        f2 = self.phone2feature[p2]

        return np.sum((f1 == f2) * self.weights) / np.sum(self.weights)

    def most_similar(self, target_phone, phone_cands):

        max_phone = phone_cands[0]
        max_score = -1000000

        if target_phone in phone_cands:
            return target_phone

        target_phone = self.normalize(target_phone)

        # if feature not found, then just use the first phone_cand
        if target_phone not in self.phone2feature:
            return phone_cands[0]

        target_feature = self.phone2feature[target_phone]

        weight_sum = np.sum(self.weights)

        for orig_phone in phone_cands:
            phone = self.normalize(orig_phone)

            if phone in self.phone2feature:
                cand_feature = self.phone2feature[phone]
                score = np.sum((target_feature == cand_feature) * self.weights) / weight_sum

                if score > max_score:
                    max_phone = orig_phone
                    max_score = score

        return max_phone


ipa = read_ipa()