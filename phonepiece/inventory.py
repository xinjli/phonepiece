from phonepiece.config import *
from phonepiece.unit import read_unit, write_unit
from phonepiece.articulatory import *
from phonepiece.bin.download_model import download_model
import json
from collections import defaultdict


def read_inventory(lang_id, model_name='latest'):
    """
    read inventory of the lang_id from a prebuilt inventory model or a customized local path

    :param lang_id: a 3 char iso id
    :param model_name: model name or a customized path
    :type lang_id_or_path:
    :return:
    :rtype:
    """

    # windows does not allow prn and con directory name
    if lang_id in ['prn', 'con']:
        lang_id = '_' + lang_id

    # check whether a customized path is used or not
    if (Path(model_name) / lang_id).exists():
        lang_dir = Path(model_name) / lang_id
    else:
        lang_dir = PhonePieceConfig.data_path / 'model' / model_name / lang_id

        # if not exists, we try to download the model
        if not lang_dir.exists():
            download_model(model_name)

        if not lang_dir.exists():
            raise ValueError(f"could not download or read {model_name} inventory")

    phone_unit = read_unit(lang_dir / 'phone.txt')
    phoneme_unit = read_unit(lang_dir / 'phoneme.txt')
    phone2phoneme = defaultdict(list)

    # use allophone file if allovera supports it
    for line in open(lang_dir / 'allophone.txt', encoding='utf-8'):
        fields = line.strip().split()
        phoneme = fields[0]

        for phone in fields[1:]:
            phone2phoneme[phone].append(phoneme)

    # blk and eos would be considered as phone/phonemes as well
    phone2phoneme['<blk>'] = ['<blk>']
    phone2phoneme['<eos>'] = ['<eos>']

    return Inventory(lang_id, model_name, phoneme_unit, phone_unit, phone2phoneme)


def write_inventory(inv, inv_path):

    inv_path = Path(inv_path)
    inv_path.mkdir(parents=True, exist_ok=True)

    write_unit(inv.phone, inv_path / 'phone.txt')
    write_unit(inv.phoneme, inv_path / 'phoneme.txt')

    allophone = dict()

    for k,v in inv.phone2phoneme.items():
        for phoneme in v:
            if phoneme not in allophone:
                allophone[phoneme] = []

            allophone[phoneme].append(k)

    w = open(inv_path / 'allophone.txt', 'w')

    for phoneme in inv.phoneme.elems[1:-1]:
        w.write(phoneme+' '+' '.join(allophone[phoneme])+'\n')

    w.close()


def is_inventory_available(lang_id, model_name='latest'):

    # check whether a customized path is used or not
    if (Path(model_name) / lang_id).exists():
        return True
    else:
        lang_dir = PhonePieceConfig.data_path / 'model' / model_name / lang_id
        return lang_dir.exists()


class Inventory:

    def __init__(self, lang_id, model_name, phoneme, phone, phone2phoneme):
        self.lang_id = lang_id
        self.phoneme = phoneme
        self.phone = phone
        self.phone2phoneme = phone2phoneme

        self.articulatory = None
        self.nearest_mapping = dict()

    def __str__(self):
        return f"<Inventory {self.lang_id} phoneme: {len(self.phoneme)}, phone: {len(self.phone)}>"

    def __repr__(self):
        return self.__str__()

    def remap(self, phonemes):

        remapped_phonemes = []
        for phoneme in phonemes:
            remapped_phonemes.append(self.get_nearest_phoneme(phoneme))

        return remapped_phonemes

    def get_nearest_phoneme(self, phoneme):
        """
        map a random phoneme (may not exist in the inventory) to the nearest phoneme in the inventory.
        The decision is based on the articulatory distance

        :param phoneme: a random phoneme
        :type phoneme: str
        :return: nearest phoneme
        :rtype: str
        """

        if self.articulatory is None:
            self.articulatory = Articulatory()

        # special handling for :
        if phoneme.endswith('ː') and phoneme[:-1] in self.phoneme.unit_to_id:
            self.nearest_mapping[phoneme] = phoneme[:-1]
            return phoneme[:-1]

        if phoneme in self.nearest_mapping:
            nearest_phoneme = self.nearest_mapping[phoneme]

        else:

            target_phonemes = list(self.phoneme.unit_to_id.keys())[1:-1]
            nearest_phoneme = self.articulatory.most_similar(phoneme, target_phonemes)
            self.nearest_mapping[phoneme] = nearest_phoneme

        return nearest_phoneme