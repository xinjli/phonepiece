from phonepiece.config import *
from phonepiece.unit import read_unit, write_unit, create_unit
from phonepiece.ipa import read_ipa
from phonepiece.iso import normalize_lang_id
from collections import defaultdict
from phonepiece.utils import load_lang_dir


def read_inventory(lang_id_or_path, model_name='latest', base=False):
    """
    read inventory of the lang_id from a prebuilt inventory model or a customized local path

    :param lang_id: a 3 char or 2 char iso id
    :param model_name: model name or a customized path
    :type lang_id_or_path:
    :return:
    :rtype:
    """

    # special handling for 'ipa' id, which returns a language-independent standard ipa set
    if lang_id_or_path == 'ipa':
        return read_ipa_inventory()

    if Path(lang_id_or_path).exists():
        lang_dir = Path(lang_id_or_path).resolve()
        lang_id = lang_dir.stem

        model_name = 'customized'

        # extract lang_id automatically
        if lang_id == 'inventory':
            lang_id = lang_dir.parent.stem

            if len(lang_id) != 2 and len(lang_id) != 3:
                lang_id = 'unknown'

    else:
        # load or download lang dir
        assert len(lang_id_or_path) == 2 or len(lang_id_or_path) == 3

        lang_id = lang_id_or_path
        lang_dir = load_lang_dir(lang_id, model_name)

        # normalize language id (e.g: 2 char 639-1 -> 3 char 639-3)
        lang_id = normalize_lang_id(lang_id)

    ipa = None

    if not base:
        phone_unit = read_unit(lang_dir / 'phone.txt')
    else:
        ipa = read_ipa()
        phone_unit = create_unit(ipa.base_phones)

    phoneme_unit = read_unit(lang_dir / 'phoneme.txt')
    phone2phoneme = defaultdict(list)
    phoneme2phone = defaultdict(list)


    # use allophone file if allovera supports it
    for line in open(lang_dir / 'allophone.txt', encoding='utf-8'):
        fields = line.strip().split()
        phoneme = fields[0]

        for phone in fields[1:]:
            if base:
                phone = ipa.compute_base_phone(phone)

            phone2phoneme[phone].append(phoneme)
            phoneme2phone[phoneme].append(phone)

    # blk and eos would be considered as phone/phonemes as well
    phone2phoneme['<blk>'] = ['<blk>']
    phone2phoneme['<eos>'] = ['<eos>']
    phoneme2phone['<blk>'] = ['<blk>']
    phoneme2phone['<eos>'] = ['<eos>']

    return Inventory(lang_id, model_name, phoneme_unit, phone_unit, phone2phoneme, phoneme2phone)


def read_ipa_inventory():
    lang_id = 'ipa'
    model_name = 'ipa_base'

    ipa = read_ipa()

    phone_unit = create_unit(ipa.base_phones)
    phoneme_unit = create_unit(ipa.base_phones)

    phone2phoneme = defaultdict(list)
    phoneme2phone = defaultdict(list)

    for phone in phone_unit.elems:
        phone2phoneme[phone].append(phone)
        phoneme2phone[phone].append(phone)

    return Inventory(lang_id, model_name, phoneme_unit, phone_unit, phone2phoneme, phoneme2phone)


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


def create_inventory(lang_id, phoneme_lst):
    """
    a simple interfact to create an customized inventory from a phoneme set.
    Assume each phoneme is realized by the same phone

    :param lang_id:
    :type lang_id: str
    :param phoneme_lst:
    :type phoneme_lst:
    :return:
    :rtype:
    """

    phoneme_lst = sorted(list(phoneme_lst))
    phoneme_unit = create_unit(phoneme_lst)
    phone_unit = create_unit(phoneme_lst)

    phone2phoneme = defaultdict(list)
    phoneme2phone = defaultdict(list)

    for phoneme in phoneme_lst:
        phone2phoneme[phoneme] = [phoneme]
        phoneme2phone[phoneme] = [phoneme]


    # blk and eos would be considered as phone/phonemes as well
    phone2phoneme['<blk>'] = ['<blk>']
    phone2phoneme['<eos>'] = ['<eos>']
    phoneme2phone['<blk>'] = ['<blk>']
    phoneme2phone['<eos>'] = ['<eos>']

    model_name = 'customized'

    return Inventory(lang_id, model_name, phoneme_unit, phone_unit, phone2phoneme, phoneme2phone)



def is_inventory_available(lang_id, model_name='latest'):

    # check whether a customized path is used or not
    if (Path(model_name) / lang_id).exists():
        return True
    else:
        lang_dir = PhonePieceConfig.data_path / 'model' / model_name / lang_id
        return lang_dir.exists()


class Inventory:

    def __init__(self, lang_id, model_name, phoneme, phone, phone2phoneme, phoneme2phone):
        self.lang_id = lang_id
        self.phoneme = phoneme
        self.phone = phone
        self.phone2phoneme = phone2phoneme
        self.phoneme2phone = phoneme2phone
        self.model_name = model_name
        self.ipa = read_ipa()
        self.nearest_mapping = dict()
        self.phone_nearest_mapping = dict()

    def __str__(self):
        return f"<Inventory {self.lang_id} ({self.model_name}) phoneme: {len(self.phoneme)}, phone: {len(self.phone)}>"

    def __repr__(self):
        return self.__str__()

    def remap(self, phonemes_or_phones, broad=True, verbose=False):

        remapped_phones = []

        if not isinstance(phonemes_or_phones, list):
            phonemes_or_phones = self.ipa.tokenize(phonemes_or_phones)

        if broad:
            for phoneme in phonemes_or_phones:
                if phoneme is None or len(phoneme.strip()) == 0:
                    continue

                nearest_phoneme = self.get_nearest_phoneme(phoneme)

                if verbose:
                    print(f"{phoneme} -> nearest phoneme {nearest_phoneme}")

                remapped_phones.append(nearest_phoneme)
        else:
            for phone in phonemes_or_phones:
                if phone is None or len(phone.strip()) == 0:
                    continue

                nearest_phone = self.get_nearest_phone(phone)

                if verbose:
                    print(f"{phone} -> nearest phone {nearest_phone}")

                remapped_phones.append(nearest_phone)

        return remapped_phones

    def phone_to_phoneme(self, phones):
        result = []
        for phone in phones:
            phonemes = self.phone2phoneme[phone]
            result.append(phonemes[0])

        return result

    def validate(self, phonemes):
        for phoneme in phonemes:
            if phoneme not in self.phoneme:
                print("phoneme ", phoneme, " not in phoneme inventory!")
                return False

        return True

    def get_nearest_phone(self, phone, verbose=False):
        """
        map a random phone (may not exist in the inventory) to the nearest phone in the inventory.
        The decision is based on the articulatory distance

        :param phone: a random phone
        :type phone: str
        :return: nearest phone
        :rtype: str
        """

        if phone in self.phone_nearest_mapping:
            nearest_phone = self.phone_nearest_mapping[phone]
        elif phone in self.phone.unit_to_id:
            self.phone_nearest_mapping[phone] = phone
            nearest_phone = phone
        elif phone.endswith('ː') and phone[:-1] in self.phone.unit_to_id:
            # special handling for :
            self.phone_nearest_mapping[phone] = phone[:-1]
            nearest_phone = phone[:-1]

        else:
            target_phones = list(self.phone.unit_to_id.keys())[1:-1]
            nearest_phone = self.ipa.most_similar(phone, target_phones, verbose=verbose)
            self.phone_nearest_mapping[phone] = nearest_phone

        return nearest_phone

    def get_nearest_phoneme(self, phoneme):
        """
        map a random phoneme (may not exist in the inventory) to the nearest phoneme in the inventory.
        The decision is based on the articulatory distance

        :param phoneme: a random phoneme
        :type phoneme: str
        :return: nearest phoneme
        :rtype: str
        """

        if phoneme in self.nearest_mapping:
            # check cache first
            nearest_phoneme = self.nearest_mapping[phoneme]

        elif phoneme in self.phoneme.unit_to_id:
            nearest_phoneme = phoneme
            self.nearest_mapping[phoneme] = phoneme

        elif phoneme.endswith('ː') and phoneme[:-1] in self.phoneme.unit_to_id:
            # special handling for :
            self.nearest_mapping[phoneme] = phoneme[:-1]
            nearest_phoneme = phoneme[:-1]

        else:

            target_phonemes = list(self.phoneme.unit_to_id.keys())[1:-1]
            nearest_phoneme = self.ipa.most_similar(phoneme, target_phonemes)
            self.nearest_mapping[phoneme] = nearest_phoneme

        return nearest_phoneme