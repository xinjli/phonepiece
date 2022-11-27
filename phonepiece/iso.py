from iso639 import languages

# map macro lang to its individual lang with the largest population or simply the first child entry on Wikipedia
_macro_to_individual = {
    'zho': 'cmn',
    'ara': 'arb',
    'aze': 'azb',
    'fas': 'pes',
    'msa': 'zlm',
    'ori': 'ory',
    'kok': 'gom',
    'srd': 'sro',
    'est': 'ekk'
}

def normalize_lang_id(lang_id):

    if len(lang_id) == 3:

        # macro to individual language normalization
        if lang_id in _macro_to_individual:
            return _macro_to_individual[lang_id]

        return lang_id

    assert len(lang_id) == 2

    language = languages.get(part1=lang_id)
    iso3 = language.part3
    if iso3 in _macro_to_individual:
        return _macro_to_individual[iso3]
    return iso3