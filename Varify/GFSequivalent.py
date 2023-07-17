

import numpy as np
# import shuffleGeneration.strategyOne


def varify(branch, perm, target_perm):

    for condition in conditionS:
        # condition = tuple(condition)
        inverse_perm = [-1 for _ in range(branch)]
        for i, c in enumerate(condition):
            inverse_perm[c] = i

        judge_perm = [-1 for _ in range(branch)]
        for j in range(branch):
            judge_perm[j] = inverse_perm[perm[condition[j]]]

        if tuple(judge_perm) in target_perm:
            print('\n\n === Optimal === \n\n')
            return True

    print('\n\n === Improve === \n\n')
    return False


if __name__ == '__main__':

    conditionS = np.load(r"D:\NutCloud\Improve_Shuffle_in_GFS\DrawingPaper\FileUpdate\GFSimproveShffule"
                         r"\shuffleGeneration\ConditionalShuffles\16_BranchConditionalShuffles.npy")

    opShuffle = [(9, 6, 13, 0, 11, 2, 15, 4, 3, 10, 7, 8, 1, 12, 5, 14),
                 (1, 6, 7, 0, 9, 2, 15, 4, 5, 14, 3, 8, 13, 10, 11, 12)]

    iniShuffle = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    twineShuffle = (5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14)
    lblockShuffle = (5, 4, 3, 0, 13, 6, 1, 2, 7, 12, 11, 8, 5, 14, 9, 10)

    varify(16, lblockShuffle, opShuffle)