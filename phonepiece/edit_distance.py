import sys

def print_result(string_lst, out=None):

    res = ""
    for str in string_lst:
        res += '{0: >5}'.format(str)

    out.write(res+'\n')

def fuzzy_match(pattern, text):
    """
    find the best edit distance

    :param string_a: pattern
    :param string_b: text
    :return: matched string part
    """

    string_b = pattern
    string_a = text

    # length of each string
    len_a = len(string_a)
    len_b = len(string_b)

    # dp table
    # its contents is edit distance, dx, dy to the best previous path
    dp = [[(0, -1, -1) for x in range(len_a+1)] for y in range(len_b+1)]

    # initialize first row and first column
    for i in range(len_a+1):
        dp[0][i] = [0, 0, 0]

    for i in range(len_b+1):
        dp[i][0] = [i, -1, 0]

    # dp update
    for i in range(1, len_b+1):
        for j in range(1, len_a+1):
            index_a = j-1
            index_b = i-1
            cost = 0 if string_a[index_a] == string_b[index_b] else 1

            dx = 0
            dy = 0
            mincost = 0

            if dp[i-1][j][0] < dp[i][j-1][0]:
                dx = -1
                dy = 0
                mincost = dp[i-1][j][0] + 1
            else:
                dx = 0
                dy = -1
                mincost = dp[i][j-1][0] + 1

            if dp[i-1][j-1][0] + cost < mincost:
                dx = -1
                dy = -1
                mincost = dp[i-1][j-1][0] + cost

            dp[i][j] = [mincost, dx, dy]


    mincost = 10000000
    best_start_index = 0
    best_end_index = len_b

    for i in range(len_a+1):
        if dp[len_b][i][0] < mincost:
            mincost = dp[len_b][i][0]
            best_end_index = i


    # backward to get the best_start_index
    cx = len_b
    cy = best_end_index

    while cx != 0:
        dx = dp[cx][cy][1]
        dy = dp[cx][cy][2]

        cx += dx
        cy += dy

    best_start_index = cy
    best_end_index -= 1

    return mincost, best_start_index, best_end_index

def edit_distance(string_a, string_b, utt_id='utt_id', verbose=False, out=None):

    # length of each string
    len_a = len(string_a)
    len_b = len(string_b)

    # dp table
    dp = [[0 for x in range(len_a+1)] for y in range(len_b+1)]
    path = [[(0, 0) for x in range(len_a+1)] for y in range(len_b+1)]

    # initialize first row and first column
    for i in range(1, len_a+1):
        dp[0][i] = i
        path[0][i] = (0, i-1)

    for i in range(1, len_b+1):
        dp[i][0] = i
        path[i][0] = (i-1, 0)

    # dp update
    for i in range(1, len_b+1):
        for j in range(1, len_a+1):
            index_a = j-1
            index_b = i-1
            cost = 0.0 if string_a[index_a] == string_b[index_b] else 1.0

            dp[i][j] = dp[i-1][j-1]+cost
            path[i][j] = (i-1,j-1)

            if dp[i][j] > dp[i-1][j]+1:
                dp[i][j] = dp[i-1][j]+1
                path[i][j] = (i-1,j)

            if dp[i][j] > dp[i][j-1]+1:
                dp[i][j] = dp[i][j-1]+1
                path[i][j] = (i, j-1)

    hyp_lst = []
    ref_lst = []
    ops_lst = []

    cur_node = (len_b, len_a)

    add_cnt = 0
    sub_cnt = 0
    del_cnt = 0

    add_lst = []
    del_lst = []
    sub_lst = []

    while(cur_node != (0,0)):
        prev_node = path[cur_node[0]][cur_node[1]]

        # substitution or match
        if prev_node[0]+1 == cur_node[0] and prev_node[1]+1 == cur_node[1]:
            hyp_lst.append(string_b[cur_node[0]-1])
            ref_lst.append(string_a[cur_node[1]-1])

            if string_a[cur_node[1]-1] == string_b[cur_node[0]-1]:
                ops_lst.append('')
            else:
                sub_lst.append((string_a[cur_node[1]-1], string_b[cur_node[0]-1]))
                ops_lst.append('Sub')
                sub_cnt += 1

        # addition
        if prev_node[0] + 1 == cur_node[0] and prev_node[1] == cur_node[1]:
            hyp_lst.append(string_b[cur_node[0]-1])
            ref_lst.append('')
            ops_lst.append('Add')
            add_lst.append(string_b[cur_node[0]-1])
            add_cnt += 1

        # deletion
        if prev_node[0] == cur_node[0] and prev_node[1]+1 == cur_node[1]:
            hyp_lst.append('')
            ref_lst.append(string_a[cur_node[1]-1])
            ops_lst.append('Del')
            del_lst.append(string_a[cur_node[1]-1])
            del_cnt += 1

        cur_node = prev_node


    if verbose:

        if out is None:
            out = sys.stdout
        out.write("-"*80+'\n')
        out.write(f"UTT: {utt_id} - add {add_cnt}, del {del_cnt}, sub {sub_cnt}\n")
        hyp_lst.append("HYP: ")
        ref_lst.append("REF: ")
        ops_lst.append("OPS: ")

        hyp_lst.reverse()
        ref_lst.reverse()
        ops_lst.reverse()

        print_result(ref_lst, out)
        print_result(hyp_lst, out)
        print_result(ops_lst, out)

    return dp[len_b][len_a], add_cnt, del_cnt, sub_cnt, add_lst, del_lst, sub_lst


def wer(string_a, string_b):

    # length of each string
    len_a = len(string_a)
    len_b = len(string_b)

    # dp table
    dp = [[0 for x in range(len_a+1)] for y in range(len_b+1)]

    # initialize first row and first column
    for i in range(len_a+1):
        dp[0][i] = i

    for i in range(len_b+1):
        dp[i][0] = i

    # dp update
    for i in range(1, len_b+1):
        for j in range(1, len_a+1):
            index_a = j-1
            index_b = i-1
            cost = 0.0 if string_a[index_a] == string_b[index_b] else 1.0
            dp[i][j] = min(dp[i-1][j-1]+cost, min(dp[i-1][j]+1, dp[i][j-1]+1))

    return dp[len_b][len_a]



def group_edit_distance(string_b, string_a, grp_dict, grp_err, grp_cnt):
    # length of each string
    len_a = len(string_a)
    len_b = len(string_b)

    # dp table
    dp = [[0 for x in range(len_a + 1)] for y in range(len_b + 1)]
    best_path = [[(0, 0) for x in range(len_a + 1)] for y in range(len_b + 1)]

    # initialize first row and first column
    for i in range(len_a + 1):
        dp[0][i] = i
        best_path[0][i] = (0, i - 1)

    for i in range(len_b + 1):
        dp[i][0] = i
        best_path[i][0] = (i - 1, 0)

    # dp update
    for i in range(1, len_b + 1):
        for j in range(1, len_a + 1):
            index_a = j - 1
            index_b = i - 1
            cost = 0.0 if string_a[index_a] == string_b[index_b] else 1.0
            dp[i][j] = min(dp[i - 1][j - 1] + cost, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))

            # get best path
            if dp[i - 1][j - 1] + cost == dp[i][j]:
                if cost == 0:
                    best_path[i][j] = (i - 1, j - 1)
                else:
                    best_path[i][j] = (-1, -1)

            elif dp[i][j] + 1 == dp[i - 1][j] + 1:
                best_path[i][j] = (i - 1, j)
            else:
                best_path[i][j] = (i, j - 1)

    # compute errors
    i = len_b
    j = len_a

    while i > 0 or j > 0:
        index_b = i - 1
        if best_path[i][j] == (i - 1, j - 1):
            grp_cnt[grp_dict[string_b[index_b]]] += 1
            i = i-1
            j = j-1
        elif best_path[i][j] == (-1, -1):
            #grp_cnt[grp_dict[string_b[index_b]]] += 1
            #grp_err[grp_dict[string_b[index_b]]] += 1

            i = i-1
            j = j-1
        elif best_path[i][j] == (i - 1, j):
            grp_cnt[grp_dict[string_b[index_b]]] += 1
            grp_err[grp_dict[string_b[index_b]]] += 1

            i, j = best_path[i][j]

        else:

            i, j = best_path[i][j]


def analyze_group_edit_distance(ans_path, hyp_path, grp_path):
    ans = dict()
    hyp = dict()

    grp_set = dict()
    grp_err = dict()
    grp_cnt = dict()

    for line in open(ans_path):
        utt_id, sent = line.split(' ', 1)
        words = sent.split()

        if '<unk>' in words:
            continue

        ans[utt_id] = words


    for line in open(hyp_path):
        utt_id, sent = line.split(' ', 1)
        words = sent.split()

        if '<unk>' in words:
            continue

        hyp[utt_id] = words

    for i, line in enumerate(open(grp_path)):
        phonemes = line.split()

        for phone in phonemes:
            grp_set[phone] = i
            grp_err[i] = 0
            grp_cnt[i] = 0

    for k, v in ans.items():
        if k not in hyp:
            print("Not found ", k, ' in hypothesis')
            continue
        group_edit_distance(ans[k], hyp[k], grp_set, grp_err, grp_cnt)

    for i in range(2):
        print("group ", i, "  wer: ", grp_err[i] * 100.0 / grp_cnt[i])
