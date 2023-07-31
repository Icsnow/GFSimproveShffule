# import pickle
#
# import numpy as np
# # import shuffleGeneration.strategyOne
#
#
# def varify(branch, perm, target_perm):
#
#     for condition in conditionS:
#         # condition = tuple(condition)
#         inverse_perm = [-1 for _ in range(branch)]
#         for i, c in enumerate(condition):
#             inverse_perm[c] = i
#
#         judge_perm = [-1 for _ in range(branch)]
#         for j in range(branch):
#             judge_perm[j] = inverse_perm[perm[condition[j]]]
#
#         judge_perm = tuple(judge_perm)
#
#         if judge_perm in target_perm:
#             print('\n\n === Optimal === \n\n')
#             return True
#
#     print('\n\n === Improve === \n\n')
#     return False
#
#
# if __name__ == '__main__':
#
#     conditionS = np.load(r"D:\NutCloud\Improve_Shuffle_in_GFS\DrawingPaper\FileUpdate\GFSimproveShffule\shuffleGeneration\ConditionalShuffles\16_BranchConditionalShuffles.npy")
#
#     with open(r"D:\NutCloud\Improve_Shuffle_in_GFS\DrawingPaper\FileUpdate\GFSimproveShffule\shuffleEvaluation\ResultDiffusion\16_branch.pkl", 'rb') as f:
#         opShuffle = pickle.load(f)
#     print(len(opShuffle))
#
#     iniShuffle = (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14)
#     twineShuffle = (5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14)
#     lblockShuffle = (5, 4, 3, 0, 13, 6, 1, 2, 7, 12, 11, 8, 15, 14, 9, 10)
#
#     varify(16, lblockShuffle, opShuffle)