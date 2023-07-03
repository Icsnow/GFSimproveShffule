import numpy as np
from tqdm import tqdm
import gurobipy as gp
from gurobipy import GRB
import multiprocessing
import pickle
import math


from _diffusion import DR_max_Search
from _differential import generate_Differential_Model
# from _linear import generate_Linear_Model
# from _impossible_differential import generate_impossibleDifferential_Model
# from _DS_MITM import gen_DSMITM_model
# from _division_property import gen_divisionProperty_model


class Evaluation:
    def __init__(self, inflowFilePath, outflowFilePath, branch):
        self.branch = branch
        self.inflowFilePath = inflowFilePath
        self.outflowFilePath = outflowFilePath

    def save_file(self, obj):
        with open(self.outflowFilePath[:-4] + '.pkl', 'wb') as fp:
            pickle.dump(obj, fp)

        with open(self.outflowFilePath, 'w+') as f:
            for k, v in obj.items():
                f.write(str(k) + ' : ' + str(v) + '\n')

    def diffusion(self):
        shuffles = np.load(self.inflowFilePath)
        diffusion_result = dict()
        for s in tqdm(shuffles):
            diffusion_result[tuple(s)] = [DR_max_Search(s)]
        diffusion_result = dict(sorted(diffusion_result.items(), key=lambda key:(key[1])))

        self.save_file(diffusion_result)
    def differential(self):
        with open(self.inflowFilePath, 'rb') as fp:
            shuffles = pickle.load(fp)
        for sk, v in shuffles.items():
            if v[0] > 2 * math.log(self.branch, 2) + 3:
                continue
            v.append(int(generate_Differential_Model(sk)))

        self.save_file(shuffles)


def Diffusion():
    # Collect the DR_max of each shuffle
    for br in branchList:
        pairEqCSPath = r"../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy".format(br)
        savePath = r'ResultDiffusion/{}_branch.txt'.format(br)
        Skive = Evaluation(pairEqCSPath, savePath, br)
        Skive.diffusion()

def Differential():
    # Collect the Min Active S_box of shuffle with lower DR_max
    for br in branchList:
        diffusedShufflePath = r'ResultDiffusion/{}_branch.pkl'.format(br)
        savePath = r'ResultDifferential/{}_branch.txt'.format(br)
        Skive = Evaluation(diffusedShufflePath, savePath, br)
        Skive.differential()


if __name__ == '__main__':
    # [4, 6, 8, 10, 12, 14, 16]
    branchList = [4, 6, 8, 10, 12, 14, 16]

    Diffusion()

    Differential()

    print('\n======\n Done \n======\n')







# def call_back(result):
#     # if result >= 20:
#     fw.write(str(perm) + ' ==> ' + str(result) + '\n')


# if __name__ == '__main__':
#
#     BranchList = [4, 6, 8, 10, 12, 14, 16]
#     for branch in BranchList:
#         fw = open(r'ResultDiffusion/{}_branch.txt'.format(branch), 'w+')
#         pool = multiprocessing.Pool(4)
#         shuffles = np.load(r"../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy".format(branch))
#         for perm in shuffles:
#             pool.apply_async(DR_max_Search, args=(perm, ), callback=call_back)
#         pool.close()
#         pool.join()
