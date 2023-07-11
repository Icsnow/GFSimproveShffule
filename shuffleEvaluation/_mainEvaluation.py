import time

import numpy as np
from tqdm import tqdm
import gurobipy as gp
from gurobipy import GRB
import multiprocessing
import pickle
import math


from _diffusion import DR_max_Search
from _differential import generate_Differential_Model
from _linear import generate_Linear_Model
from _impossible_differential import generate_impossibleDifferential_Model
from _zc_linear import generate_zcLinear_Model
from _DS_MITM import gen_DSMITM_model
# from _division_property import solve_divisionProperty_model


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

        border = shuffles.get(next(iter(shuffles)))[0]
        differential_result = dict()
        for sk, v in shuffles.items():
            if v[0] <= border:
                differential_result[sk] = v + [int(generate_Differential_Model(sk))]
            else:
                break
        differential_result = dict(sorted(differential_result.items(), key=lambda key:(key[1][1]), reverse=True))

        self.save_file(differential_result)

    def linear(self):
        with open(self.inflowFilePath, 'rb') as fp:
            shuffles = pickle.load(fp)
        border = shuffles.get(next(iter(shuffles)))[1] - step
        linear_result = dict()
        for sk, v in shuffles.items():
            if v[1] > border:
                linear_result[sk] = v + [int(generate_Linear_Model(sk))]
            else:
                break
        linear_result = dict(sorted(linear_result.items(), key=lambda key: (key[1][2]), reverse=True))

        self.save_file(linear_result)

    def impossibleDifferential(self):
        with open(self.inflowFilePath, 'rb') as fp:
            shuffles = pickle.load(fp)
        border = [-1,
                  shuffles.get(next(iter(shuffles)))[1] - step,
                  shuffles.get(next(iter(shuffles)))[2] - step]
        idc_result = dict()
        for sk, v in shuffles.items():
            if all(border[i] < v[i] for i in range(3)):
                for t_round in range(5, 99):
                    ac_position = np.eye(self.branch)
                    flag = 0
                    for ac_in in ac_position:
                        for ac_out in ac_position:
                            if generate_impossibleDifferential_Model(sk, t_round, ac_in, ac_out) == 3:
                                flag = 1
                                break
                        if flag: break
                    if not flag:
                        idc_result[sk] = v + [t_round]
                        break
        idc_result = dict(sorted(idc_result.items(), key=lambda  key:(key[1][3])))
        self.save_file(idc_result)

    def zc_linear(self):
        with open(self.inflowFilePath, 'rb') as fp:
            shuffles = pickle.load(fp)
        border = [-1,
                  shuffles.get(next(iter(shuffles)))[1] - step,
                  shuffles.get(next(iter(shuffles)))[2] - step,
                  shuffles.get(next(iter(shuffles)))[3] - step]
        zcl_result = dict()
        for sk, v in shuffles.items():
            if all(border[i] < v[i] for i in range(4)):
                for t_round in range(5, 99):
                    ac_position = np.eye(self.branch)
                    flag = 0
                    for ac_in in ac_position:
                        for ac_out in ac_position:
                            if generate_zcLinear_Model(sk, t_round, ac_in, ac_out) == 3:
                                flag = 1
                                break
                        if flag: break
                    if not flag:
                        zcl_result[sk] = v + [t_round]
                        break
        zcl_result = dict(sorted(zcl_result.items(), key=lambda  key:(key[1][4])))
        self.save_file(zcl_result)

    def ds_mitm(self):
        with open(self.inflowFilePath, 'rb') as fp:
            shuffles = pickle.load(fp)
        degree = -1
        result_ds_mitm = dict()
        border = [shuffles.get(next(iter(shuffles)))[0],
                  shuffles.get(next(iter(shuffles)))[1],
                  shuffles.get(next(iter(shuffles)))[2],
                  shuffles.get(next(iter(shuffles)))[3],
                  shuffles.get(next(iter(shuffles)))[4]]
        for sk, v in shuffles.items():
            if all(abs(v[i] - border[i] < step) for i in range(5)):
                for r_round in range(5, 99):
                    model = gen_DSMITM_model(r_round, self.branch, sk)
                    model.optimize()
                    if model.Status == 2:
                        degree = model.Objval
                    else:
                        result_ds_mitm[sk] = v + [(r_round, int(degree))]
                        break
        result_ds_mitm = dict(sorted(result_ds_mitm.items(), key=lambda  key:(key[1][5])))
        self.save_file(result_ds_mitm)

'''
Methods of 
'''


def Diffusion():
    # Collect the DR_max of each shuffle
    pool = multiprocessing.Pool(4)
    for br in tqdm(branchList):
        pairEqCSPath = r"../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy".format(br)
        savePath = r'ResultDiffusion/{}_branch.txt'.format(br)
        Skive = Evaluation(pairEqCSPath, savePath, br)
        # Skive.diffusion()
        pool.apply_async(Skive.diffusion, args=())
    pool.close()
    pool.join()


def Differential():
    # Collect the Min Truncated DC Active S_box of shuffle with lower DR_max
    # diffBorderList = [2 * (math.log(br, 2)) for br in branchList]
    pool = multiprocessing.Pool(4)
    for br in branchList:
        diffusedShufflePath = r'ResultDiffusion/{}_branch.pkl'.format(br)
        savePath = r'ResultDifferential/{}_branch.txt'.format(br)
        Skive = Evaluation(diffusedShufflePath, savePath, br)
        # Skive.differential()
        pool.apply_async(Skive.differential)
    pool.close()
    pool.join()


def Linear():
    # Collect the Min Truncated LC Active S_box of shuffle with higher ADs
    pool = multiprocessing.Pool(4)
    for br in branchList:
        differentialShufflePath = r'ResultDifferential/{}_branch.pkl'.format(br)
        savePath = r'ResultLinear/{}_branch.txt'.format(br)
        Skive = Evaluation(differentialShufflePath, savePath, br)
        # Skive.linear()
        pool.apply_async(Skive.linear)
    pool.close()
    pool.join()


def ImpossibleDifferential():
    # Collect the Longest Truncated IDC Propagation of shuffle with higher ADs & ALs
    pool = multiprocessing.Pool(4)
    for br in branchList:
        linearShufflePath = r'ResultLinear/{}_branch.pkl'.format(br)
        savePath = r'ResultImpossibleDifferential/{}_branch.txt'.format(br)
        Skive = Evaluation(linearShufflePath, savePath, br)
        # Skive.impossibleDifferential()
        pool.apply_async(Skive.impossibleDifferential, args=())
    pool.close()
    pool.join()


def ZeroCorrespondLinear():
    # Collect the Longest Truncated ZC Propagation of shuffle with longer IDC trail
    pool = multiprocessing.Pool(4)
    for br in branchList:
        idcShufflePath = r'ResultImpossibleDifferential/{}_branch.pkl'.format(br)
        savePath = r'ResultZCLinear/{}_branch.txt'.format(br)
        Skive = Evaluation(idcShufflePath, savePath, br)
        # Skive.zc_linear()
        pool.apply_async(Skive.zc_linear, args=())
    pool.close()
    pool.join()


def DS_MITM():
    pool = multiprocessing.Pool(4)
    for br in branchList:
        impossibleDifferentialShufflePath = r'ResultZCLinear/{}_branch.pkl'.format(br)
        savePath = r'ResultDSMITM/{}_branch.txt'.format(br)
        Skive = Evaluation(impossibleDifferentialShufflePath, savePath, br)
        # Skive.ds_mitm()
        pool.apply_async(Skive.ds_mitm, args=())
    pool.close()
    pool.join()


def Integral():


if __name__ == '__main__':
    # [4, 6, 8, 10, 12, 14, 16]
    branchList = [4, 6, 8, 10]

    # number of shuffle classes may pick when each evaluation
    step = 3
    times = time.time()

    # Diffusion()
    # Differential()
    # Linear()
    # ImpossibleDifferential()
    # ZeroCorrespondLinear()
    # DS_MITM()
    Integral

    print('\n======\n Done \n======\n')
    print('TimeCost: ', time.time() - times)


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
