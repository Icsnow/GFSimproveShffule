# import time
#
# import numpy as np
# from tqdm import tqdm
# import gurobipy as gp
# from gurobipy import GRB
# import multiprocessing
# import pickle
# import math
#
#
# from _diffusion import DR_max_Search
# from _differential import generate_Differential_Model
# from _linear import generate_Linear_Model
# from _impossible_differential import generate_impossibleDifferential_Model
# from _zc_linear import generate_zcLinear_Model
# from _DS_MITM import gen_DSMITM_model
# from _division_property import DivisionProperty
#
#
# class Evaluation:
#     def __init__(self, inflowFilePath, outflowFilePath, branch):
#         self.branch = branch
#         self.inflowFilePath = inflowFilePath
#         self.outflowFilePath = outflowFilePath
#         with open(self.inflowFilePath, 'rb') as fp:
#             self.shuffles = pickle.load(fp)
#
#     def save_file(self, obj):
#         with open(self.outflowFilePath, 'wb') as fp:
#             pickle.dump(obj, fp)
#
#         with open(self.outflowFilePath[:-4] + '.txt', 'w+') as f:
#             for k, v in obj.items():
#                 f.write(str(k) + ' : ' + str(v) + '\n')
#
#     def diffusion(self):
#         shuffles = np.load(self.inflowFilePath)
#         diffusion_result = dict()
#         for s in tqdm(shuffles):
#             diffusion_result[tuple(s)] = [DR_max_Search(s)]
#         diffusion_result = dict(sorted(diffusion_result.items(), key=lambda key:(key[1])))
#
#         self.save_file(diffusion_result)
#
#     def differential(self):
#
#         border = self.shuffles.get(next(iter(self.shuffles)))[0]
#         differential_result = dict()
#         for sk, v in self.shuffles.items():
#             if v[0] <= border:
#                 differential_result[sk] = v + [int(generate_Differential_Model(sk))]
#             else:
#                 break
#         differential_result = dict(sorted(differential_result.items(), key=lambda key: (key[1][1]), reverse=True))
#
#         self.save_file(differential_result)
#
#     def linear(self):
#         border = self.shuffles.get(next(iter(self.shuffles)))[1]
#         linear_result = dict()
#         for sk, v in self.shuffles.items():
#             if abs(v[1] - border) < 3:
#                 linear_result[sk] = v + [int(generate_Linear_Model(sk))]
#             else:
#                 break
#         linear_result = dict(sorted(linear_result.items(), key=lambda key: (key[1][2]), reverse=True))
#
#         self.save_file(linear_result)
#
#     def impossibleDifferential(self):
#         border = [self.shuffles.get(next(iter(self.shuffles)))[0],
#                   self.shuffles.get(next(iter(self.shuffles)))[1],
#                   self.shuffles.get(next(iter(self.shuffles)))[2]]
#         idc_result = dict()
#         for sk, v in self.shuffles.items():
#             if all(abs(border[i] - v[i]) < 3 for i in range(3)):
#                 for t_round in range(5, 99):
#                     ac_position = np.eye(self.branch)
#                     flag = 0
#                     for ac_in in ac_position:
#                         for ac_out in ac_position:
#                             if generate_impossibleDifferential_Model(sk, t_round, ac_in, ac_out) == 3:
#                                 flag = 1
#                                 break
#                         if flag:
#                             break
#                     if not flag:
#                         idc_result[sk] = v + [t_round]
#                         break
#         idc_result = dict(sorted(idc_result.items(), key=lambda key: (key[1][3])))
#         self.save_file(idc_result)
#
#     def zc_linear(self):
#         border = [self.shuffles.get(next(iter(self.shuffles)))[0],
#                   self.shuffles.get(next(iter(self.shuffles)))[1],
#                   self.shuffles.get(next(iter(self.shuffles)))[2],
#                   self.shuffles.get(next(iter(self.shuffles)))[3]]
#         zcl_result = dict()
#         for sk, v in self.shuffles.items():
#             if all(abs(border[i] - v[i]) < 3 for i in range(4)):
#                 for t_round in range(5, 99):
#                     ac_position = np.eye(self.branch)
#                     flag = 0
#                     for ac_in in ac_position:
#                         for ac_out in ac_position:
#                             if generate_zcLinear_Model(sk, t_round, ac_in, ac_out) == 3:
#                                 flag = 1
#                                 break
#                         if flag: break
#                     if not flag:
#                         zcl_result[sk] = v + [t_round]
#                         break
#         zcl_result = dict(sorted(zcl_result.items(), key=lambda key: (key[1][4])))
#         self.save_file(zcl_result)
#
#     def ds_mitm(self):
#         # degree = -1
#         result_ds_mitm = dict()
#         border = [self.shuffles.get(next(iter(self.shuffles)))[0],
#                   self.shuffles.get(next(iter(self.shuffles)))[1],
#                   self.shuffles.get(next(iter(self.shuffles)))[2],
#                   self.shuffles.get(next(iter(self.shuffles)))[3],
#                   self.shuffles.get(next(iter(self.shuffles)))[4]]
#         for sk, v in self.shuffles.items():
#             if all(abs(border[i] - v[i] < 3) for i in range(5)):
#                 for r_round in range(5, 99):
#                     model = gen_DSMITM_model(r_round, self.branch, sk)
#                     model.optimize()
#                     # if model.Status == 2:
#                     #     degree = model.Objval
#                     # else:
#                     if model.Status == 3:
#                         # infeasible
#                         result_ds_mitm[sk] = v + [r_round]  # (r_round, int(degree))
#                         break
#         result_ds_mitm = dict(sorted(result_ds_mitm.items(), key=lambda key: (key[1][5])))
#         self.save_file(result_ds_mitm)
#
#     # def divisionProperty(self):
#     #     border = [-1,
#     #               self.shuffles.get(next(iter(self.shuffles)))[1],
#     #               self.shuffles.get(next(iter(self.shuffles)))[2],
#     #               self.shuffles.get(next(iter(self.shuffles)))[3],
#     #               self.shuffles.get(next(iter(self.shuffles)))[4],
#     #               self.shuffles.get(next(iter(self.shuffles)))[5]]
#     #     result_integral = dict()
#     #     for sk, v in self.shuffles.items():
#     #         if all(abs(border[i] - v[i] < 2) for i in range(6)):
#     #             r = 10
#     #             while r < 20:
#     #                 dvp = DivisionProperty(r, sk, 1)
#     #                 if dvp.solve_model():
#     #                     r += 1
#     #                     continue
#     #                 else:
#     #                     result_integral[sk] = v + [r-1]
#     #                     break
#     #         result_integral = dict(sorted(result_integral.items(), key=lambda key: (key[1][6])))
#     #         self.save_file(result_integral)
#
#
# def Diffusion():
#     # Collect the DR_max of each shuffle
#     pool = multiprocessing.Pool(4)
#     for br in tqdm(branchList):
#         pairEqCSPath = r"../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy".format(br)
#         savePath = r'ResultDiffusion/{}_branch.pkl'.format(br)
#         Skive = Evaluation(pairEqCSPath, savePath, br)
#         # Skive.diffusion()
#         pool.apply_async(Skive.diffusion, args=())
#     pool.close()
#     pool.join()
#
#
# def Differential():
#     # Collect the Min Truncated DC Active S_box of shuffle with lower DR_max
#     # diffBorderList = [2 * (math.log(br, 2)) for br in branchList]
#     pool = multiprocessing.Pool(4)
#     for br in branchList:
#         diffusedShufflePath = r'ResultDiffusion/{}_branch.pkl'.format(br)
#         savePath = r'ResultDifferential/{}_branch.pkl'.format(br)
#         Skive = Evaluation(diffusedShufflePath, savePath, br)
#         # Skive.differential()
#         pool.apply_async(Skive.differential)
#     pool.close()
#     pool.join()
#
#
# def Linear():
#     # Collect the Min Truncated LC Active S_box of shuffle with higher ADs
#     pool = multiprocessing.Pool(4)
#     for br in branchList:
#         differentialShufflePath = r'ResultDifferential/{}_branch.pkl'.format(br)
#         savePath = r'ResultLinear/{}_branch.pkl'.format(br)
#         Skive = Evaluation(differentialShufflePath, savePath, br)
#         Skive.linear()
#         pool.apply_async(Skive.linear, args=())
#     pool.close()
#     pool.join()
#
#
# def ImpossibleDifferential():
#     # Collect the Longest Truncated IDC Propagation of shuffle with higher ADs & ALs
#     for br in branchList:
#         linearShufflePath = r'ResultLinear/{}_branch.pkl'.format(br)
#         savePath = r'ResultImpossibleDifferential/{}_branch.pkl'.format(br)
#         Skive = Evaluation(linearShufflePath, savePath, br)
#         Skive.impossibleDifferential()
#
#
# def ZeroCorrespondLinear():
#     # Collect the Longest Truncated ZC Propagation of shuffle with longer IDC trail
#     for br in branchList:
#         idcShufflePath = r'ResultImpossibleDifferential/{}_branch.pkl'.format(br)
#         savePath = r'ResultZCLinear/{}_branch.pkl'.format(br)
#         Skive = Evaluation(idcShufflePath, savePath, br)
#         Skive.zc_linear()
#
#
# def DS_MITM():
#     for br in branchList:
#         impossibleDifferentialShufflePath = r'ResultZCLinear/{}_branch.pkl'.format(br)
#         savePath = r'ResultDSMITM/{}_branch.pkl'.format(br)
#         Skive = Evaluation(impossibleDifferentialShufflePath, savePath, br)
#         Skive.ds_mitm()
#
#
# # def Division_Property():
# #     for br in branchList:
# #         dsMITMShufflePath = r'ResultDSMITM/{}_branch.pkl'.format(br)
# #         savePath = r'ResultIntegral/{}_branch.pkl'.format(br)
# #         Skive = Evaluation(dsMITMShufflePath, savePath, br)
# #         Skive.divisionProperty()
#
#
# if __name__ == '__main__':
#     # [4, 6, 8, 10, 12, 14, 16]
#     branchList = [4]
#
#     # number of shuffle classes may pick when each evaluation
#     step = 3
#
#     times = time.time()
#
#     # open these: ↓
#
#     # Diffusion()
#     # Differential()
#     # Linear()
#     # ImpossibleDifferential()
#     # ZeroCorrespondLinear()
#     # DS_MITM()
#
#     # evaluate the **integral attacks** individually
#     # Division_Property()
#
#     print('\n======\n Done \n======\n')
#     print('TimeCost: ', time.time() - times)
#
