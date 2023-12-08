

import gurobipy as gp
from gurobipy import GRB
import pickle
import time
from tqdm import tqdm
from tools import save_file


def gen_DSMITM_model(ROUND, BRANCH, SHUFFLE):

    m = gp.Model('DS-MITM')
    m.setParam('OutputFlag', 0)
    x = m.addVars(ROUND+1, BRANCH, vtype=GRB.BINARY, name='TypeX')
    y = m.addVars(ROUND+1, BRANCH, vtype=GRB.BINARY, name='TypeY')
    z = m.addVars(ROUND, int(BRANCH/2), vtype=GRB.BINARY, name='TypeZ')

    # forward differential X
    for r in range(ROUND):
        # XOR
        for b in range(BRANCH)[::2]:
            m.addConstr(x[r, b] + x[r, b+1] - x[r+1, SHUFFLE[b+1]] >= 0, name='')
            m.addConstr(2 * x[r+1, SHUFFLE[b+1]] - x[r, b] - x[r, b+1] >= 0, name='')
        # SHUFFLE
        for b in range(BRANCH)[::2]:
            m.addConstr(x[r, b] == x[r+1, SHUFFLE[b]], name='')

    # backward determine Y
    for r in range(1, ROUND+1)[::-1]:
        # branch
        for b in range(BRANCH)[::2]:
            m.addConstr(y[r, SHUFFLE[b]] + y[r, SHUFFLE[b+1]] - y[r-1, b] >= 0, name='')
            m.addConstr(2 * y[r-1, b] - y[r, SHUFFLE[b]] - y[r, SHUFFLE[b+1]] >= 0, name='')
        # SHUFFLE
        for b in range(1, BRANCH)[::2]:
            m.addConstr(y[r, SHUFFLE[b]] == y[r-1, b], name='')

    # z x=y=1, z=1, else z=0
    for r in range(ROUND):
        for b in range(int(BRANCH/2)):
            m.addConstr(x[r, 2*b] >= z[r, b], name='')
            m.addConstr(y[r, 2*b+1] >= z[r, b], name='')
            m.addConstr(-x[r, 2*b] - y[r, 2*b+1] + z[r, b] + 1 >= 0, name='')

    # additional constraints:
    # initial x,y >= 1
    m.addConstr(sum(x[0, b] for b in range(BRANCH)) >= 1, name='')
    m.addConstr(sum(y[ROUND, b] for b in range(BRANCH)) >= 1, name='')

    # NO.ac_cells <= NO.(Key_length(=2 * branch_size)/size_cells, 2 for TWINE-128, 1.25 for TWINE-80)
    m.addConstr(sum(z[r, b] for b in range(int(BRANCH/2)) for r in range(ROUND)) <= 2 * BRANCH-1, name='')

    # obj function
    m.setObjective(sum(z[r, b] for b in range(int(BRANCH/2)) for r in range(ROUND)), GRB.MINIMIZE)
    # m.write('DS-MITM_model.lp')
    return m


if __name__ == '__main__':

    time_start = time.time()
    br_list = [4, 6, 8, 10, 12, 14, 16]

    for br in br_list:
        with open(r"ResultDiffusion/{}_branch_diffusion_filtered.pkl".format(br), 'rb') as f:
            SHUFFLES = pickle.load(f)
        # SHUFFLES = {(9, 6, 13, 0, 11, 2, 15, 4, 3, 10, 7, 8, 1, 12, 5, 14): [8],
        #             (1, 6, 7, 0, 9, 2, 15, 4, 5, 14, 3, 8, 13, 10, 11, 12): [8]}
        result = dict()
        border = SHUFFLES.get(next(iter(SHUFFLES)))[-1]
        for sk, v in tqdm(SHUFFLES.items()):
            # degAB = -1
            if abs(v[-1] - border) < 3:
                for r_round in range(5, 30):
                    b_branch = len(sk)
                    model = gen_DSMITM_model(r_round, b_branch, sk)
                    model.optimize()
                    # if model.Status == 2:
                    #     degAB = model.Objval

                    if model.Status == 3:
                        result[sk] = v + [r_round - 1] #, int(degAB)
                        break
        save_file(result, r'ResultDSMITM/{}_branch_DSMITM_filtered'.format(br), False)
        # if t_round go to 29, the corresponding shuffle will be discarded.

        # for s in result:
        #     print(s, ': ', result[s], ',')
    # print('\n\n ===\n time cost: ' + str(time.time() - time_start), '\n === \n\n')
