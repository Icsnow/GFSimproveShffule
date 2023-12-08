

import pickle
import numpy as np


def rev(pp):
    p_new = [-1 for _ in range(len(pp))]
    for i in pp:
        p_new[i] = pp.index(i)
    return p_new


def save_file(a_dict, outflow, reverse):
    """
    save the result into binary files and readable files
    """
    if reverse:
        a_dict = dict(sorted(a_dict.items(), key=lambda key: (key[1][-1]), reverse=True))
    else:
        a_dict = dict(sorted(a_dict.items(), key=lambda key: (key[1][-1])))
    with open(outflow+'.pkl', 'wb+') as fb:
        pickle.dump(a_dict, fb)
    with open(outflow+'.txt', 'w+') as ft:
        for sk, v in a_dict.items():
            ft.write(str(sk) + ': ' + str(v) + '\n')


def verify(branch, perm, target_perm):
    """
    check weather the shuffle in the optimal shuffle set
    """

    conditions = np.load(r'..\shuffleGeneration\ConditionalShuffles\{}_BranchConditionalShuffles.npy'.format(branch))
    for condition in conditions:
        # condition = tuple(condition)
        inverse_perm = [-1 for _ in range(branch)]
        for i, c in enumerate(condition):
            inverse_perm[c] = i

        judge_perm = [-1 for _ in range(branch)]
        for j in range(branch):
            judge_perm[j] = inverse_perm[perm[condition[j]]]

        judge_perm = tuple(judge_perm)

        if judge_perm in target_perm:
            # print('\n\n === IN ===')
            # print(perm, '=', judge_perm, '<==>', target_perm[judge_perm])
            # print(judge_perm)
            return True

    # print('\n\n === OUT === \n\n')
    return False

def cycleDecompose(permutation):
    """
    cycle decomposition of shuffles
    """
    pos = 0
    deg = 1
    while True:
        # print(pos, end=',')
        pos = permutation[pos]
        if pos != 0:
            deg += 1
        else:
            break
    if deg == len(permutation):
        print(permutation)


if __name__ == '__main__':

    # optimal_shuffles = [(9, 6, 13, 0, 11, 2, 15, 4, 3, 10, 7, 8, 1, 12, 5, 14)]
    optimal_shuffles = [(1, 12, 9, 0, 5, 2, 15, 4, 11, 6, 3, 8, 7, 10, 13, 14)]
    judge_shuffles = optimal_shuffles[:]

    # target_shuffle = [(1, 6, 7, 0, 9, 2, 15, 4, 5, 14, 3, 8, 13, 10, 11, 12)]
    target_shuffle = [(1, 4, 13, 0, 7, 2, 9, 10, 3, 6, 15, 8, 11, 12, 5, 14)]
    br = len(judge_shuffles[0])

    for s in optimal_shuffles:
        print(verify(br, s, target_shuffle) or verify(br, rev(s), target_shuffle))
