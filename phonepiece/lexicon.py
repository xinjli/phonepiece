from collections import defaultdict
from phonepiece.utils import load_lang_dir
from phonepiece.lang import normalize_lang_id
from phonepiece.inventory import read_inventory
from phonepiece.utils import import_with_auto_install
from phonepiece.arpa import ArpaConverter


def read_lexicon(lang_id, model_name='latest'):

    """
    read lexicon of the lang_id from a prebuilt inventory model or a customized local path

    :param lang_id: a 3 char or 2 char iso id
    :param model_name: model name or a customized path
    :type lang_id_or_path:
    :return:
    :rtype:
    """

    # normalize language id (e.g: 2 char 639-1 -> 3 char 639-3)
    lang_id = normalize_lang_id(lang_id)

    # load or download lang dir
    lang_dir = load_lang_dir(lang_id, model_name)

    inventory = read_inventory(lang_id, model_name)

    lexicon_path = lang_dir / 'lexicon.txt'

    # special handling for English
    if lang_id == 'eng':
        cmudict_module = import_with_auto_install('cmudict', 'cmudict')
        cmudict = cmudict_module.dict()
        converter = ArpaConverter()
        word2phoneme = {}
        for word in cmudict:
            arpa = cmudict[word][0]
            ipas = converter.convert(arpa)
            word2phoneme[word] = ipas

        return Lexicon(lang_id, inventory, word2phoneme)

    elif not lexicon_path.exists():
        # empty lexicon
        return Lexicon(lang_id, inventory, {})

    word2phoneme = {}
    for line in open(str(lexicon_path), 'r', encoding='utf-8'):
        fields = line.strip().split('\t')

        # wrongly formatted lines
        if len(fields) != 2 or len(fields[0]) == 0 or len(fields[1]) == 0:
            continue

        # to lower by default
        word = fields[0].lower()
        phonemes = fields[1].split()
        remapped_phonemes = inventory.remap(phonemes)
        word2phoneme[word] = remapped_phonemes

    return Lexicon(lang_id, inventory, word2phoneme)


def write_lexicon(lexicon, lexicon_path):

    wfile = open(str(lexicon_path), 'w', encoding='utf-8')

    for word, units in lexicon.word_to_unit.items():
        wfile.write(word+' '+' '.join(units)+'\n')

    wfile.close()


class Lexicon:

    def __init__(self, lang_id, inventory, word2phoneme):

        self.lang_id = lang_id

        # word to id
        self.word2phoneme = word2phoneme

        self.inventory = inventory

    def __str__(self):
        return f'<Lexicon: {len(self.word2phoneme)} words>'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.word2phoneme)

    def __contains__(self, item):
        return item.lower() in self.word2phoneme

    def __getitem__(self, item):
        return self.word2phoneme[item.lower()]