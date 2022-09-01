import panphon
import numpy as np
from phonepiece.config import PhonePieceConfig

class Articulatory:

    def __init__(self):

        self.feature_table = {}

        lines = open(PhonePieceConfig.data_path / 'phoible-segments-features.tsv', 'r', encoding='utf-8').readlines()
        for line in lines[1:]:

            fields = line.strip().split('\t')
            phone = fields[0]

            feats = []
            for field in fields[1:]:
                if field == '0':
                    feats.append(0)
                elif field == '-':
                    feats.append(-1)
                elif field == '+':
                    feats.append(1)
                else:
                    feats.append(0)

            assert len(feats) == 37

            self.feature_table[phone] = np.array(feats)


    def feature(self, phone):
        if phone not in self.feature_table:
            return np.zeros(37)

        #assert phone in self.feature_table, " phone "+phone+" not available in the table"

        return self.feature_table[phone]

    def similarity(self, p1, p2):
        """
        similarity between phone 1 and phone 2

        :param p1:
        :param p2:
        :return:
        """
        return np.inner(self.feature(p1), self.feature(p2))

    def most_similar(self, target_phone, phone_cands):

        max_phone = None
        max_score = -1000000

        target_feature = self.feature(target_phone)

        for phone in phone_cands:
           score = np.inner(self.feature(phone), target_feature)

           if score > max_score:
               max_phone = phone
               max_score = score

        return max_phone


class PanphoneArticulatory:

    def __init__(self):

        self.feature_table = panphon.FeatureTable()

    def feature(self, phone):

        try:
            feats = self.feature_table.word_to_vector_list(phone, numeric=True)
        except:
            if len(phone) == 2:
                phone = phone[0]+' '+phone[1]
                feats = self.feature_table.word_to_vector_list(phone, numeric=True)
            else:
                feats = []

        if len(feats) == 0:
            feats = np.zeros(22)
        else:
            feats = np.array(feats[0], dtype=np.float32)

        return feats

    def similarity(self, p1, p2):
        """
        similarity between phone 1 and phone 2

        :param p1:
        :param p2:
        :return:
        """
        return np.inner(self.feature(p1), self.feature(p2))

    def most_similar(self, target_phone, phone_cands):

        max_phone = None
        max_score = -1000000

        target_feature = self.feature(target_phone)

        for phone in phone_cands:
           score = np.inner(self.feature(phone), target_feature)

           if score > max_score:
               max_phone = phone
               max_score = score

        return max_phone