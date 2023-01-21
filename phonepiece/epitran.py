from phonepiece.iso import normalize_lang_id
from phonepiece.config import PhonePieceConfig
from collections import defaultdict
import unicodedata
import csv
from phonepiece.utils import load_lang_dir
import re
from phonepiece.ipa import read_ipa


def read_epitran_g2p(lang_id_or_g2p_id, writing_system=None):

    if '-' in lang_id_or_g2p_id:
        fields = lang_id_or_g2p_id.split('-')
        assert len(fields) == 2

        lang_id = fields[0]
        writing_system = fields[1]
    else:
        lang_id = normalize_lang_id(lang_id_or_g2p_id)

    lang_dir = load_lang_dir(lang_id)
    g2p_dir = lang_dir / 'g2p'

    if writing_system is not None:
        g2p_path = g2p_dir / f"{lang_id}-{writing_system}.csv"
        assert g2p_path.exists(), f"{lang_id}-{writing_system} does not exist!"

    else:
        if g2p_dir.exists():
            g2p_ids = sorted([p.stem for p in list(g2p_dir.glob('*'))])
        else:
            g2p_ids = []

        assert len(g2p_ids) > 0, "provided lang_id " + lang_id + " is not supported by epitran"

        if len(g2p_ids) > 1:
            print(f"there are multiple g2p_ids {g2p_ids}, we use the first {g2p_ids[0]}")

        g2p_id = g2p_ids[0]
        g2p_path = g2p_dir / (g2p_id+".csv")

    g2p = defaultdict(list)

    ipa = read_ipa()

    with open(g2p_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        orth, phon = next(reader)
        if orth != 'Orth' or phon != 'Phon':
            raise DatafileError(f'Header is ["{orth}", "{phon}"] instead of ["Orth", "Phon"].')
        for (i, fields) in enumerate(reader):
            try:
                graph, phons = fields
            except ValueError as malformed_data_file:
                raise DatafileError(f'Map file is not well formed at line {i + 2}.') from malformed_data_file

            phons = ipa.tokenize(phons)
            for phon in phons:
                graph = unicodedata.normalize('NFC', graph)
                phon = unicodedata.normalize('NFC', phon)
                phon = re.sub('[˩˨˧˦˥]', '', phon)
                g2p[graph].append(phon)

    return g2p