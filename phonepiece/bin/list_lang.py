import sys
from pathlib import Path
from phonepiece.lang import read_all_langs, read_lang_name
from phonepiece.inventory import read_inventory
from phonepiece.lexicon import read_lexicon
import argparse


if __name__ == '__main__':

    print("| language ISO id     |  language name     |")
    print("|---------------------|--------------------|")
    for lang in sorted(read_all_langs()):
        try:
            print(f"| {lang:8s} | {read_lang_name(lang)} |")
        except:
            pass