import sys
from pathlib import Path
from phonepiece.distance import phonological_distance, fast_edit_distance, edit_distance
import argparse
from tqdm import tqdm
from collections import Counter

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read the contents of two files.')
    parser.add_argument( '--hyp', help='the path to the hypothesis file')
    parser.add_argument('--ref', help='the path to the reference file')
    parser.add_argument('-f', '--format', default='kaldi', help='kaldi or text')
    parser.add_argument('-o', '--output', help='the path to the reference file')
    parser.add_argument('-v', '--verbose', type=bool ,default=False)

    args = parser.parse_args()
    output = args.output
    ref = args.ref
    hyp = args.hyp
    verbose = args.verbose
    file_format = args.format

    assert file_format in ['kaldi', 'text']

    w = None
    if output is not None:
        Path(output).parent.mkdir(exist_ok=True, parents=True)
        w = open(output, "w")

    expect_label = {}

    for i, line in enumerate(open(ref, 'r')):
        fields = line.strip().split()

        if file_format == 'kaldi':
            utt_id = fields[0]
            expect_label[utt_id] = fields[1:]
        else:
            utt_id = f"{i:05d}"
            expect_label[utt_id] = fields

    tot_len_cnt = 0
    tot_err_cnt = 0
    tot_dst_cnt = 0
    tot_add_cnt = 0
    tot_sub_cnt = 0
    tot_del_cnt = 0

    add_counter = Counter()
    del_counter = Counter()
    sub_counter = Counter()

    for i, line in tqdm(enumerate(open(hyp, 'r').readlines())):
        fields = line.strip().split()

        if file_format == 'kaldi':
            utt_id = fields[0]
            hyp = fields[1:]
        else:
            utt_id = f"{i:05d}"
            hyp = fields

        if utt_id not in expect_label:
            continue

        ref = expect_label[utt_id]

        dst_cnt = phonological_distance(ref, hyp)
        all_cnt = len(expect_label[utt_id])

        if verbose:
            err_cnt, add_cnt, del_cnt, sub_cnt, add_lst, del_lst, sub_lst = edit_distance(ref, hyp, utt_id=utt_id, verbose=verbose, out=w)
            tot_add_cnt += add_cnt
            tot_del_cnt += del_cnt
            tot_sub_cnt += sub_cnt
            add_counter.update(add_lst)
            del_counter.update(del_lst)
            sub_counter.update(sub_lst)

        else:
            err_cnt = fast_edit_distance(ref, hyp)

        tot_err_cnt += err_cnt
        tot_dst_cnt += dst_cnt
        tot_len_cnt += all_cnt

    print(f"------------------------------------")
    print(f"TOTAL ERR: {tot_err_cnt}\n")
    print(f"TOTAL DST: {tot_dst_cnt}\n")
    print(f"TOTAL LEN: {tot_len_cnt}\n")

    if verbose:
        print(f"TOTAL ADD {tot_add_cnt:.3f}: {add_counter.most_common(10)}")
        print(f"TOTAL DEL {tot_del_cnt:.3f}: {del_counter.most_common(10)}")
        print(f"TOTAL SUB {tot_sub_cnt:.3f}: {sub_counter.most_common(10)}")

    if tot_len_cnt != 0:
        print(f"TOTAL ERR RATE: {tot_err_cnt/tot_len_cnt:.3f}")
        if verbose:
            print(f"TOTAL ADD RATE: {tot_add_cnt/tot_len_cnt:.3f}")
            print(f"TOTAL DEL RATE: {tot_del_cnt/tot_len_cnt:.3f}")
            print(f"TOTAL SUB RATE: {tot_sub_cnt/tot_len_cnt:.3f}")

        print(f"TOTAL DST RATE: {tot_dst_cnt/tot_len_cnt:.3f}")
    print(f"------------------------------------")

    if w is not None:
        w.write(f"------------------------------------")
        w.write(f"TOTAL ERR: {tot_err_cnt}\n")
        w.write(f"TOTAL DST: {tot_dst_cnt}\n")
        w.write(f"TOTAL LEN: {tot_len_cnt}\n")

        if verbose:
            w.write(f"TOTAL ADD {tot_add_cnt:.3f}: {add_counter.most_common(10)})\n")
            w.write(f"TOTAL DEL {tot_del_cnt:.3f}: {del_counter.most_common(10)})\n")
            w.write(f"TOTAL SUB {tot_sub_cnt:.3f}: {sub_counter.most_common(10)})\n")

        if tot_len_cnt != 0:
            w.write(f"TOTAL ERR RATE: {tot_err_cnt/tot_len_cnt:.3f}\n")

            if verbose:
                w.write(f"TOTAL ADD RATE: {tot_add_cnt / tot_len_cnt:.3f}\n")
                w.write(f"TOTAL DEL RATE: {tot_del_cnt / tot_len_cnt:.3f}\n")
                w.write(f"TOTAL SUB RATE: {tot_sub_cnt / tot_len_cnt:.3f}\n")

            w.write(f"TOTAL DST RATE: {tot_dst_cnt/tot_len_cnt:.3f}\n")

        w.write(f"------------------------------------\n")
        w.close()