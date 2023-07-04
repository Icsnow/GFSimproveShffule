

import gurobipy as gp
from gurobipy import GRB
import numpy as np


def generate_impossibleDifferential_Model(shuffle, Round, activate_bit_input, activate_bit_output):
    Branch = len(shuffle)
    inverse_shuffle = [shuffle.index(i) for i in range(Branch)]

    # Variables
    m = gp.Model('Truncated Impossible Differential Evaluation')
    x_in = m.addVars(1, Branch, vtype=GRB.BINARY, name='x')

    midRound = [(r, b) for b in range(Branch)[::2] for r in range(1, Round+1)]
    x = m.addVars(midRound, vtype=GRB.BINARY, name='x')

    # Initial constraint
    # 要写出限制每一bit而不能一起等于1
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

    m.write('impossible_differential.lp')
    m.optimize()
    return m.Status


if __name__ == '__main__':
    for t_round in range(5, 30):
        branch = 6
        ac_position = np.eye(6)

        for ac_in in ac_position:
            for ac_out in ac_position:
                # print(ac_in, ac_out)
                if generate_impossibleDifferential_Model([1, 2, 5, 0, 3, 4], t_round, ac_in, ac_out) == 2:
                    print('===\n', t_round, '\n===')
                    break
