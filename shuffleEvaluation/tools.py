

import pickle
import numpy as np
import _diffusion
import _DS_MITM
import _impossible_differential
import _zc_linear
import _differential
import _linear
import _division_property


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


def varify(branch, perm, target_perm):
    """
    check weather the shuffle in the optimal shuffle set
    """

    conditions = np.load(r'..\shuffleGeneration\ConditionalShuffles\16_BranchConditionalShuffles.npy')
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
            print('\n\n === IN ===')
            print(judge_perm, target_perm[judge_perm])
            return

    print('\n\n === OUT === \n\n')
    return


def cycleDecompose(permutation):
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


def dvCheck(shuffle):
    for sk in shuffle:
        r = 10
        while r < 30:
            varify_flag = True
            for ac in range(1, 16):
                dp = _division_property.DivisionProperty(r, sk, ac, )
                if dp.solve_model():
                    break
                else:
                    varify_flag = False
            if not varify_flag:
                print(r - 1)
                break
            else:
                r += 1


if __name__ == '__main__':

    # example = (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14)
    # Shi = [(15, 2, 13, 4, 11, 6, 3, 8, 1, 10, 5, 0, 7, 12, 9, 14),
    #        (7, 2, 13, 4, 15, 6, 1, 8, 5, 10, 3, 0, 11, 12, 9, 14),
    #        (15, 2, 9, 4, 1, 6, 11, 8, 3, 10, 13, 0, 7, 12, 5, 14),
    #        (7, 2, 11, 4, 9, 6, 1, 8, 15, 10, 13, 0, 3, 12, 5, 14),
    #        (13, 2, 15, 4, 11, 6, 3, 8, 1, 10, 5, 0, 9, 12, 7, 14),
    #        (7, 2, 11, 4, 9, 6, 1, 8, 13, 10, 15, 0, 5, 12, 3, 14),
    #        (13, 2, 9, 4, 1, 6, 11, 8, 3, 10, 15, 0, 5, 12, 7, 14),
    #        (7, 2, 15, 4, 13, 6, 1, 8, 5, 10, 3, 0, 9, 12, 11, 14),
    #        (9, 2, 7, 4, 11, 6, 15, 8, 13, 10, 5, 0, 1, 12, 3, 14),
    #        (5, 2, 9, 4, 13, 6, 15, 8, 3, 10, 7, 0, 1, 12, 11, 14),
    #        (9, 2, 7, 4, 11, 6, 13, 8, 15, 10, 5, 0, 3, 12, 1, 14),
    #        (5, 2, 9, 4, 15, 6, 13, 8, 3, 10, 7, 0, 11, 12, 1, 14)]
    # twine = (5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14)
    # lblock = (15, 4, 3, 0, 13, 6, 1, 2, 7, 12, 11, 8, 5, 14, 9, 10)
    #
    # condition_S = np.load(r'..\shuffleGeneration\ConditionalShuffles\16_BranchConditionalShuffles.npy')
    #
    # with open(r'ResultDifferential\16_branch_dc.pkl', 'rb') as fb:
    #     target_S = pickle.load(fb)
    #
    # for s in Shi:
    #     varify(16, s, target_S)

    Shieq = [(5, 10, 9, 0, 13, 2, 15, 4, 3, 6, 7, 8, 1, 12, 11, 14)]
    dvCheck(Shieq)
    # print(_linear.generate_Linear_Model(Shieq))


# ====================================== Division Property ========================================== #



