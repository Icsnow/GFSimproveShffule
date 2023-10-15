

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time
import pickle
import tools
from tqdm import tqdm


def generate_impossibleDifferential_Model(shuffle, Round, activate_bit_input, activate_bit_output):
    Branch = len(shuffle)
    inverse_shuffle = [shuffle.index(i) for i in range(Branch)]

    # Variables
    m = gp.Model('Truncated Impossible Differential Evaluation')
    m.setParam('OutputFlag', 0)
    x_in = m.addVars(1, Branch, vtype=GRB.BINARY, name='x')

    midRound = [(r, b) for b in range(Branch)[::2] for r in range(1, Round+1)]
    x = m.addVars(midRound, vtype=GRB.BINARY, name='x')

    # Initial constraint
    for i in range(Branch):
        m.addConstr(x_in[0, i] == activate_bit_input[i], name='')
    for j in range(Branch)[::2]:
        m.addConstr(x[Round - 1, j] == activate_bit_output[j+1], name='')
        m.addConstr(x[Round, j] == activate_bit_output[j], name='')

    # XOR constraint
    # first round
    for b in range(Branch)[::2]:
        m.addConstr(x_in[0, b] + x_in[0, b + 1] - x[1, shuffle[b + 1]] >= 0, name='')
        m.addConstr(x_in[0, b] - x_in[0, b + 1] + x[1, shuffle[b + 1]] >= 0, name='')
        m.addConstr(- x_in[0, b] + x_in[0, b + 1] + x[1, shuffle[b + 1]] >= 0, name='')

        m.addConstr(x[1, b] + x_in[0, inverse_shuffle[b + 1]] - x[2, shuffle[b + 1]] >= 0, name='')
        m.addConstr(x[1, b] - x_in[0, inverse_shuffle[b + 1]] + x[2, shuffle[b + 1]] >= 0, name='')
        m.addConstr(- x[1, b] + x_in[0, inverse_shuffle[b + 1]] + x[2, shuffle[b + 1]] >= 0, name='')

    # middle round
    for r in range(2, Round):
        for b in range(Branch)[::2]:
            m.addConstr(x[r, b] + x[r - 1, inverse_shuffle[b + 1]] - x[r + 1, shuffle[b + 1]] >= 0, name='')
            m.addConstr(x[r, b] - x[r - 1, inverse_shuffle[b + 1]] + x[r + 1, shuffle[b + 1]] >= 0, name='')
            m.addConstr(- x[r, b] + x[r - 1, inverse_shuffle[b + 1]] + x[r + 1, shuffle[b + 1]] >= 0, name='')

    # m.write('impossible_differential.lp')
    m.optimize()
    return m.Status


if __name__ == '__main__':
    # time_start = time.time()

    br_list = [4, 6, 8, 10, 12, 14, 16]
    for br in br_list:
        with open(r"ResultDSMITM/{}_branch_DSMITM.pkl".format(br), 'rb') as f:
            SHUFFLES = pickle.load(f)

        # SHUFFLES = {
        # (7, 2, 13, 4, 15, 6, 1, 8, 5, 10, 3, 0, 11, 12, 9, 14) :  [8, 13] ,
        # (9, 2, 7, 4, 11, 6, 13, 8, 15, 10, 5, 0, 3, 12, 1, 14) :  [8, 13] ,
        # (5, 2, 9, 4, 15, 6, 13, 8, 3, 10, 7, 0, 11, 12, 1, 14) :  [8, 13] ,
        # (13, 2, 15, 4, 11, 6, 3, 8, 1, 10, 5, 0, 9, 12, 7, 14) :  [8, 13] ,
        # (5, 2, 9, 4, 13, 6, 15, 8, 3, 10, 7, 0, 1, 12, 11, 14) :  [8, 13] ,
        # (13, 2, 9, 4, 1, 6, 11, 8, 3, 10, 15, 0, 5, 12, 7, 14) :  [8, 13] ,
        # (15, 2, 9, 4, 1, 6, 11, 8, 3, 10, 13, 0, 7, 12, 5, 14) :  [8, 13] ,
        # (7, 2, 15, 4, 13, 6, 1, 8, 5, 10, 3, 0, 9, 12, 11, 14) :  [8, 13] ,
        # (15, 2, 13, 4, 11, 6, 3, 8, 1, 10, 5, 0, 7, 12, 9, 14) :  [8, 13] ,
        # (7, 2, 11, 4, 9, 6, 1, 8, 13, 10, 15, 0, 5, 12, 3, 14) :  [8, 13] ,
        # (7, 2, 11, 4, 9, 6, 1, 8, 15, 10, 13, 0, 3, 12, 5, 14) :  [8, 13] ,
        # (9, 2, 7, 4, 11, 6, 15, 8, 13, 10, 5, 0, 1, 12, 3, 14) :  [8, 13]
        # }

        result = dict()
        border = [SHUFFLES.get(next(iter(SHUFFLES)))[0],
                  SHUFFLES.get(next(iter(SHUFFLES)))[1]]
        for sk, v in tqdm(SHUFFLES.items()):
            if all(abs(v[i] - border[i]) < 3 for i in range(2)):
                for t_round in range(5, 30):
                    ac_position = np.eye(br)
                    flag = 0
                    for ac_in in ac_position:
                        for ac_out in ac_position:
                            if generate_impossibleDifferential_Model(sk, t_round, ac_in, ac_out) == 3:
                                flag = 1
                                break
                        if flag:
                            break
                    if not flag:
                        result[sk] = v + [t_round]
                        break
        tools.save_file(result, r'ResultImpossibleDifferential/{}_branch_idc'.format(br), False)
        # for s in result:
        #     print(s, ': ', result[s], ',')
    # print(time.time() - time_start)
