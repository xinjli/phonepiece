import numpy as np
from phonepiece.articulatory import Articulatory


def read_unit(unit_path):
    # load unit from units.txt
    # units.txt should start from index 1 (because ctc blank is taking the 0 index)

    unit_to_id = dict()

    unit_to_id['<blk>'] = 0

    idx = 0

    for line in open(str(unit_path), 'r', encoding='utf-8'):
        fields = line.strip().split()

        assert len(fields) < 3

        if len(fields) == 1:
            unit = fields[0]
            idx += 1
        else:
            unit = fields[0]
            idx = int(fields[1])

        unit_to_id[unit] = idx

    if '<eos>' not in unit_to_id:
        unit_to_id['<eos>'] = idx+1

    unit_to_id['<blk>'] = 0

    unit = Unit(unit_to_id)
    return unit


def write_unit(unit, unit_path):

    w = open(str(unit_path), 'w', encoding='utf-8')
    for i in range(1, len(unit.id_to_unit)-1):
        u = unit.id_to_unit[i]
        w.write(u+'\n')

    w.close()


def create_unit(unit_lst):

    unit_to_id = dict()

    unit_to_id['<blk>'] = 0

    idx = 0

    for i, unit in enumerate(sorted(unit_lst)):
        unit_to_id[unit] = i+1

    unit = Unit(unit_to_id)
    return unit


class Unit:

    def __init__(self, unit_to_id):
        """
        Unit manages bidirectional mapping from unit to id and id to unit
        both are dict

        :param unit_to_id:
        """

        self.unit_to_id = unit_to_id
        self.id_to_unit = {}

        assert '<blk>' in self.unit_to_id and self.unit_to_id['<blk>'] == 0

        for unit, idx in self.unit_to_id.items():
            self.id_to_unit[idx] = unit

        self.elems = list(self.id_to_unit.values())

        self.articulatory = None
        self.nearest_mapping = None

    def __str__(self):
        return '<Unit: ' + str(len(self.unit_to_id)) + ' elems: ' + str(self.unit_to_id)+ '>'

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, idx):
        return self.id_to_unit[idx]

    def __len__(self):
        return len(self.id_to_unit)

    def __contains__(self, unit):
        if unit == ' ':
            unit = '<space>'

        return unit in self.unit_to_id

    def __eq__(self, other):
        """
        compare whether two units are equivalent or not

        :param other:
        :type other:
        :return:
        :rtype:
        """
        return set(self.unit_to_id.keys()) == set(other.unit_to_id.keys())


    def atoi(self, inputs):
        if isinstance(inputs, list):
            return self.get_ids(inputs)
        else:
            return self.get_id(inputs)


    def itoa(self, inputs):
        if isinstance(inputs, list):
            return self.get_units(inputs)
        else:
            return self.get_unit(inputs)


    def get_id(self, unit):

        # handle special units
        if unit == ' ':
            unit = '<space>'

        assert unit in self.unit_to_id, 'unit '+unit+'is not in '+str(self.unit_to_id)
        return self.unit_to_id[unit]

    def get_ids(self, units):
        """
        get index for a word list
        :param words:
        :return:
        """

        return [self.get_id(unit) for unit in units]

    def get_unit(self, id):
        assert id >= 0 and id in self.id_to_unit, f"{id} not in the unit {self.id_to_unit}"

        unit = self.id_to_unit[id]

        # handle special units
        if unit == '<space>':
            unit = ' '

        return unit

    def get_units(self, ids):
        """
        get unit from ids

        :param ids: elem_id list
        :return: a list of unit
        """

        return [self.get_unit(id) for id in ids]

    def get_joint_id(self, unit):

        # handle special units
        if unit == ' ':
            unit = '<space>'

        joint_id = 0

        # if it is a combined phone "a:b"
        if ':' in unit and unit[-1] != ':':
            phones = unit.split(':')

            for phone in phones:
                joint_id *= 1000
                joint_id += self.unit_to_id[phone]

        else:
            joint_id = self.unit_to_id[unit]

        return joint_id

    def get_joint_ids(self, units):
        return [self.get_id(unit) for unit in units]

    def get_joint_unit(self, id):

        phones = []

        if id not in self.id_to_unit:

            while id > 0:
                phones.append(self.id_to_unit[id%1000])
                id //= 1000

            phones.reverse()
        else:
            phones = [self.id_to_unit[id]]

        return phones

    def get_joint_units(self, ids):
        phones = []

        for id in ids:
            phones.extend(self.get_joint_unit(id))

        return phones

    def get_nearest_unit(self, unit):

        raise NotImplementedError

    def get_nearest_phoneme(self, unit):

        if self.articulatory is None:
            self.articulatory = Articulatory()

        if self.nearest_mapping is None:
            self.nearest_mapping = dict()

        if unit in self.nearest_mapping:
            return self.nearest_mapping[unit]

        if unit in self.unit_to_id:
            self.nearest_mapping[unit] = unit
            return unit

        # special handling for :
        if unit.endswith('ː') and unit[:-1] in self.unit_to_id:
            self.nearest_mapping[unit] = unit[:-1]
            return unit[:-1]

        target_unit = list(self.unit_to_id.keys())[1:-1]
        nearest_unit = self.articulatory.most_similar(unit, target_unit)
        self.nearest_mapping[unit] = nearest_unit

        return nearest_unit