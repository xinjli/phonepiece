import re
import json
from pathlib import Path
from phonepiece.config import PhonePieceConfig


def read_tree():

    iso2path = {}

    for line in open(PhonePieceConfig.data_path / 'tree.txt', 'r'):
        fields = line.strip().split()
        iso = fields[0]
        path = fields[1].split('/')[1:]

        iso2path[iso] = path

    return LanguageTree(iso2path)


class LanguageTree:

    def __init__(self, iso2path):

        self.iso2path = iso2path

        self.iso_target = []

    def __contains__(self, item):
        return item in self.iso2path

    def setup_target_langs(self, langs):

        self.iso_target = []

        for lang in langs:
            if lang not in self.iso2path:
                print("language: ", lang, " is not a valid lang")
                continue

            self.iso_target.append(lang)

    def similarity(self, lang1, lang2):

        path1 = self.iso2path[lang1]
        path2 = self.iso2path[lang2]

        common_len = 0
        for i in range(min(len(path1), len(path2))):
            if path1[i] == path2[i]:
                common_len += 1
            else:
                break

        return common_len

    def distance(self, lang1, lang2):
        common_len = self.similarity(lang1, lang2)
        path1 = self.iso2path[lang1]
        path2 = self.iso2path[lang2]

        return len(path1)+len(path2) - common_len

    def get_nearest_lang(self, iso):

        max_score = 1
        max_lang = 'eng'

        for lang in self.iso_target:
            if iso != lang:
                score = self.similarity(iso, lang)
                if score > max_score:
                    max_score = score
                    max_lang = lang

        return max_lang

    def get_nearest_langs(self, iso, num_lang=10):

        assert iso in self.iso2path, f"language {iso} is not valid"

        score = {}

        for lang in self.iso_target:
            if iso != lang:
                score[lang] = self.similarity(iso, lang)

        lang_ids = [lang_dist[0] for lang_dist in sorted(score.items(), key=lambda x:-x[1])[:num_lang]]
        return lang_ids

    def get_similar_lang2(self, iso, num_lang=10):

        score = {}

        for lang in self.iso_target:
            if iso != lang:
                score[lang] = self.distance(iso, lang)

        return sorted(score.items(), key=lambda x:x[1])[:num_lang]