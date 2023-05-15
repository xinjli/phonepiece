import sys
from pathlib import Path
from phonepiece.lang import normalize_lang_id, read_lang_name
from phonepiece.inventory import read_inventory
import argparse
from tqdm import tqdm
from collections import Counter


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='look up language info')
    parser.add_argument('--lang', help='the path to the hypothesis file')
    parser.add_argument('--inverse', type=bool, default=False, help='phone2phoneme')

    args = parser.parse_args()
    lang_id = args.lang

    print(read_lang_name(lang_id))

    lang_id = normalize_lang_id(lang_id)
    inv = read_inventory(lang_id)

    print(f"{inv}")
    print(f"phoneme : {inv.phoneme.elems[1:-1]}")
    print(f"phone   : {inv.phone.elems[1:-1]}")

    if not args.inverse:
        for phoneme in inv.phoneme.elems[1:-1]:
            print(f"{phoneme:8s} {inv.phoneme2phone[phoneme]}")
    else:
        for phone in inv.phone.elems[1:-1]:
            print(f"{phone:8s} {inv.phone2phoneme[phone]}")
