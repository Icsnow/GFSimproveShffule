

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time
import pickle
from tools import save_file
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
        with open(r"ResultDSMITM/{}_branch_DSMITM_filtered.pkl".format(br), 'rb') as f:
            SHUFFLES = pickle.load(f)

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
        save_file(result, r'ResultImpossibleDifferential/{}_branch_idc_filtered'.format(br), False)
        # for s in result:
        #     print(s, ': ', result[s], ',')
    # print(time.time() - time_start)
