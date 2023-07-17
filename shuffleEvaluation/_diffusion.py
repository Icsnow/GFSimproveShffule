
from collections import deque
import multiprocessing
import time
import numpy
import pickle


def DR_max_Search(shuffle):
    border_round = len(shuffle)
    max_round = -1

    for i in range(border_round):
        queue = deque([i])
        diffuse_round = 1
        temp_queue = deque()

        while len(queue) < border_round and diffuse_round < border_round:
            while queue:
                node = queue.popleft()
                if node % 2 == 0 and node+1 not in queue:
                    queue.append(node+1)
                temp_queue.append(shuffle[node])

            while temp_queue:
                queue.append(temp_queue.popleft())

            diffuse_round += 1

        max_round = max(max_round, diffuse_round)
    return max_round


# if __name__ == '__main__':
#     # [4, 6, 8, 10, 12, 14, 16]
#     branchList = [4, 6, 8, 10, 12, 14, 16]
#
#     # number of shuffle classes may pick when each evaluation
#     times = time.time()
#
#     for br in branchList:
#         pairEqCSPath = r"../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy".format(br)
#         savePath = r'ResultDiffusion/{}_branch.pkl'.format(br)
#         shuffles = numpy.load(pairEqCSPath)
#
#         pool = multiprocessing.Pool(4)
#         for s in shuffles:
#             pool.apply_async(DR_max_Search, args=(s, ))
#         pool.close()
#         pool.join()
#         with open(savePath, 'wb') as fp:
#             pickle.dump(obj, fp)
#
#         with open(self.outflowFilePath[:-4] + '.txt', 'w+') as f:
#             for k, v in obj.items():
#                 f.write(str(k) + ' : ' + str(v) + '\n')
#
#     print('\n======\n Done \n======\n')
#     print('TimeCost: ', time.time() - times)
