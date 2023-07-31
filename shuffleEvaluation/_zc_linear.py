

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pickle
from tqdm import tqdm
import tools


def generate_zcLinear_Model(shuffle, Round, activate_bit_input, activate_bit_output):
    Branch = len(shuffle)
    inverse_shuffle = [shuffle.index(i) for i in range(Branch)]

    # Variables
    m = gp.Model('Multidimensional Differential Evaluation')
    m.setParam('OutputFlag', 0)
    x_in = m.addVars(1, Branch, vtype=GRB.BINARY, name='x')

    midRound = [(r, b) for b in range(1, Branch)[::2] for r in range(1, Round+1)]
    x = m.addVars(midRound, vtype=GRB.BINARY, name='x')

    # Initial constraint
    for i in range(Branch):
        m.addConstr(x_in[0, i] == activate_bit_input[i], name='')
    for j in range(1, Branch)[::2]:
        m.addConstr(x[Round - 1, j] == activate_bit_output[j - 1], name='')
        m.addConstr(x[Round, j] == activate_bit_output[j], name='')

    # 3-branch constraint
    # first round
    for b in range(Branch)[::2]:
        m.addConstr(x_in[0, b] + x_in[0, b + 1] - x[1, shuffle[b]] >= 0, name='')
        m.addConstr(x_in[0, b] - x_in[0, b + 1] + x[1, shuffle[b]] >= 0, name='')
        m.addConstr(- x_in[0, b] + x_in[0, b + 1] + x[1, shuffle[b]] >= 0, name='')

        m.addConstr(x[1, b+1] + x_in[0, inverse_shuffle[b]] - x[2, shuffle[b]] >= 0, name='')
        m.addConstr(x[1, b+1] - x_in[0, inverse_shuffle[b]] + x[2, shuffle[b]] >= 0, name='')
        m.addConstr(- x[1, b+1] + x_in[0, inverse_shuffle[b]] + x[2, shuffle[b]] >= 0, name='')

    # middle round
    for r in range(2, Round):
        for b in range(Branch)[::2]:
            m.addConstr(x[r, b+1] + x[r - 1, inverse_shuffle[b]] - x[r + 1, shuffle[b]] >= 0, name='')
            m.addConstr(x[r, b+1] - x[r - 1, inverse_shuffle[b]] + x[r + 1, shuffle[b]] >= 0, name='')
            m.addConstr(- x[r, b+1] + x[r - 1, inverse_shuffle[b]] + x[r + 1, shuffle[b]] >= 0, name='')

    # m.write('zc_linear.lp')
    m.optimize()
    return m.Status


if __name__ == '__main__':
    br_list = [4, 6, 8, 10, 12, 14, 16]
    for br in br_list:
        with open(r"ResultImpossibleDifferential/{}_branch_idc.pkl".format(br), 'rb') as f:
            SHUFFLES = pickle.load(f)
        result = dict()
        border = [SHUFFLES.get(next(iter(SHUFFLES)))[0],
                  SHUFFLES.get(next(iter(SHUFFLES)))[1],
                  SHUFFLES.get(next(iter(SHUFFLES)))[2]]
        for sk, v in tqdm(SHUFFLES.items()):
            if all(abs(v[i] - border[i]) < 3 for i in range(3)):
                for t_round in range(5, 30):
                    ac_position = np.eye(br)
                    flag = 0
                    for ac_in in ac_position:
                        for ac_out in ac_position:
                            if generate_zcLinear_Model(sk, t_round, ac_in, ac_out) == 3:
                                flag = 1
                                break
                        if flag:
                            break
                    if not flag:
                        result[sk] = v + [t_round]
                        break
        tools.save_file(result, r'ResultZCLinear/{}_branch_zc'.format(br), False)