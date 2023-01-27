# phonepiece

![CI Test](https://github.com/xinjli/phonepiece/actions/workflows/python.yml/badge.svg)

`phonepiece` is library to manage phone inventories, it also has a few linguistic/phonetics tools.

It is mainly intended to be used in the following projects, but it can be used as a standalone library

- [allosaurus](https://github.com/xinjli/allosaurus): phone recognition toolkit
- [transphone](https://github.com/xinjli/transphone): grapheme-to-phoneme toolkit
- [asr2k](https://github.com/xinjli/asr2k): speech recognition systems for 2000 languages

## Install

phonepiece is available from pip

```bash
pip install phonepiece
```
You can also clone this repository and install

```bash
python setup.py install
```

## Usage

### Inventory Lookup

The main feature of phonepiece is to look-up inventory.

An inventory typically contains the following information:

- `phoneme`: language-dependent units
- `phone`: language-independent units
- `allophone`: the mapping between phone and phoneme

A simple usage is as follows:

```python
In [1]: from phonepiece import read_inventory                                                                                                   

In [2]: eng = read_inventory('eng')                                                                                                             

In [3]: eng                                                                                                                                     
Out[3]: <Inventory eng phoneme: 40, phone: 46>

In [4]: eng.phoneme                                                                                                                             
Out[4]: <Unit: 40 elems: {'<blk>': 0, 'a': 1, 'b': 2, 'd': 3, 'd͡ʒ': 4, 'e': 5, 'f': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 's': 16, 't': 17, 't͡ʃ': 18, 'u': 19, 'v': 20, 'w': 21, 'z': 22, 'æ': 23, 'ð': 24, 'ŋ': 25, 'ɑ': 26, 'ɔ': 27, 'ə': 28, 'ɛ': 29, 'ɡ': 30, 'ɪ': 31, 'ɹ': 32, 'ɹ̩': 33, 'ʃ': 34, 'ʊ': 35, 'ʌ': 36, 'ʒ': 37, 'θ': 38, '<eos>': 39}>

In [5]: eng.phone                                                                                                                               
Out[5]: <Unit: 46 elems: {'<blk>': 0, 'a': 1, 'b': 2, 'b̥': 3, 'd': 4, 'dʒ': 5, 'd̥': 6, 'e': 7, 'f': 8, 'g': 9, 'h': 10, 'i': 11, 'j': 12, 'k': 13, 'kʰ': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'p': 19, 'pʰ': 20, 's': 21, 't': 22, 'tʃ': 23, 'tʰ': 24, 'u': 25, 'v': 26, 'w': 27, 'z': 28, 'æ': 29, 'ð': 30, 'ŋ': 31, 'ɑ': 32, 'ɔ': 33, 'ə': 34, 'ɛ': 35, 'ɡ̥': 36, 'ɪ': 37, 'ɹ': 38, 'ɹ̩': 39, 'ʃ': 40, 'ʊ': 41, 'ʌ': 42, 'ʒ': 43, 'θ': 44, '<eos>': 45}>

In [6]: eng.phoneme2phone                                                                                                                       
Out[6]: 
defaultdict(list,
            {'a': ['a'],
             'b': ['b', 'b̥'],
             'd': ['d', 'd̥'],
             'd͡ʒ': ['dʒ'],
             'e': ['e'],
             'f': ['f'],
             'h': ['h'],
             'i': ['i'],
             'j': ['j'],
             'k': ['kʰ', 'k'],
             'l': ['l'],
             'm': ['m'],
             'n': ['n'],
             'o': ['o'],
             'p': ['pʰ', 'p'],
             's': ['s'],
             't': ['tʰ', 't'],
             't͡ʃ': ['tʃ'],
             'u': ['u'],
             'v': ['v'],
             'w': ['w'],
             'z': ['z'],
             'æ': ['æ'],
             'ð': ['ð'],
             'ŋ': ['ŋ'],
             'ɑ': ['ɑ'],
             'ɔ': ['ɔ'],
             'ə': ['ə'],
             'ɛ': ['ɛ'],
             'ɡ': ['g', 'ɡ̥'],
             'ɪ': ['ɪ'],
             'ɹ': ['ɹ'],
             'ɹ̩': ['ɹ̩'],
             'ʃ': ['ʃ'],
             'ʊ': ['ʊ'],
             'ʌ': ['ʌ'],
             'ʒ': ['ʒ'],
             'θ': ['θ'],
             '<blk>': ['<blk>'],
             '<eos>': ['<eos>']})
```

### Phonetics Utilities

This lib also provides a few phonetics utilities, for example, IPA manipulations

```python
In [1]: from phonepiece.ipa import read_ipa                                                         

In [2]: ipa = read_ipa()                                                                            

In [3]: ipa.tokenize('kʰæt')                                                                        
Out[3]: ['kʰ', 'æ', 't']

In [4]: ipa.similarity('a', 'e')                                                                    
Out[4]: 0.9655172413793104
```

## Models

| model | # supported languages |                                                                          description                                                                          |
| :----: |:---------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| phoible |          ~2k          | phone/phoneme databases extracted from [Phoible](https://phoible.org/) [1]. Allophone information is from [Allovera](https://github.com/dmort27/allovera) [3] |
| latest |          ~8k          |                                               Phoible database + estimated inventory based on our LREC work [2]                                               |


## Acknowledgement

This repository use code/data from the following repository

- [epitran](https://github.com/dmort27/epitran)
- [panphon](https://github.com/dmort27/panphon)
- [allovera](https://github.com/dmort27/allovera)
- [phoible](https://github.com/phoible/dev)
- [wikipron](https://github.com/CUNY-CL/wikipron)

## Reference

- [1] Moran, Steven, Daniel McCloy, and Richard Wright. "PHOIBLE online." (2014).
- [2] Li, Xinjian, et al. "Phone Inventories and Recognition for Every Language" LREC 2022. 2022
- [3] Mortensen, David R., et al. "AlloVera: A Multilingual Allophone Database." Proceedings of the 12th Language Resources and Evaluation Conference. 2020.
