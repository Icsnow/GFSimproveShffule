import time
from collections import deque
import numpy as np
from tqdm import tqdm
import tools
from multiprocessing import Pool


def one_pos(shuffle, branch, pos):
    d_round = 1
    queue = deque([pos])
    t_queue = deque()

    while d_round < 12:
        ini_shuffle = set([i for i in range(branch)])
        while queue:
            node = queue.popleft()
            ini_shuffle.discard(node)

            if node % 2 == 0:
                queue.append(node + 1)
            t_queue.append(shuffle[node])

        if not ini_shuffle:
            break

        d_round += 1

        while t_queue:
            queue.append(t_queue.popleft())

    if d_round == 12:
        return 2 * branch
    return d_round


def dr_max(shuffle):
    ls = len(shuffle)
    max_round = []
    for i in shuffle:
        max_round.append(one_pos(shuffle, ls, i))
    return max(max_round)


def rev(pp):
    p_new = [-1 for _ in range(len(pp))]
    for i in pp:
        p_new[i] = pp.index(i)
    return p_new


if __name__ == '__main__':
    # timestart = time.time()
    br_list = [4, 6, 8, 10, 12, 14, 16]
    for br in br_list:
        SHUFFLES = np.load(r'../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy'.format(br))
        ret = []
        p = Pool(8)
        for s in SHUFFLES:
            s = tuple(s)
            A = p.apply_async(dr_max, args=(s, ))
            B = p.apply_async(dr_max, args=(rev(s), ))
            # result[s] = [max(A.get(), B.get())]
            ret.append((A.get(), B.get()))
        p.close()
        p.join()

        # print(time.time() - timestart)
        result = dict()
        for s, v in zip(SHUFFLES, ret):
            result[tuple(s)] = [max(v)]

        tools.save_file(result, r'ResultDiffusion/{}_branch_diffusion'.format(br), False)

        # for s in result:
        #     print(s, ': ', result[s], ',')

    # print(time.time() - timestart)
