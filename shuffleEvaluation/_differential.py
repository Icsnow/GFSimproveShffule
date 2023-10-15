

import gurobipy as gp
from gurobipy import GRB
import time
import pickle
from tqdm import tqdm
import tools

def generate_Differential_Model(shuffle):
    """
    Note: the shuffle are all eo-shuffle,so for all b is even positions
    x[r,b+1] from the last round (without constraints)
    """
    Round = 20
    Branch = len(shuffle)
    inverse_shuffle = [shuffle.index(i) for i in range(Branch)]

    # Variables
    m = gp.Model('Truncated Differential Evaluation')
    m.setParam('OutputFlag', 0)
    x_in = m.addVars(1, Branch, vtype=GRB.BINARY, name='x')
    midRound = [(r, b) for b in range(Branch)[::2] for r in range(1, Round+1)]
    x = m.addVars(midRound, vtype=GRB.BINARY, name='x')

    # Initial constraint
    m.addConstr(sum(x_in[0, i] for i in range(Branch)) >= 1, name='')

    # XOR constraint
    for b in range(Branch)[::2]:
        m.addConstr(x_in[0, b] + x_in[0, b+1] - x[1, shuffle[b + 1]] >= 0, name='')
        m.addConstr(x_in[0, b] - x_in[0, b+1] + x[1, shuffle[b + 1]] >= 0, name='')
        m.addConstr(- x_in[0, b] + x_in[0, b+1] + x[1, shuffle[b + 1]] >= 0, name='')

        m.addConstr(x[1, b] + x_in[0, inverse_shuffle[b + 1]] - x[2, shuffle[b + 1]] >= 0, name='')
        m.addConstr(x[1, b] - x_in[0, inverse_shuffle[b + 1]] + x[2, shuffle[b + 1]] >= 0, name='')
        m.addConstr(- x[1, b] + x_in[0, inverse_shuffle[b + 1]] + x[2, shuffle[b + 1]] >= 0, name='')

    for r in range(2, Round - 1):
        for b in range(Branch)[::2]:
            m.addConstr(x[r, b] + x[r-1, inverse_shuffle[b+1]] - x[r+1, shuffle[b+1]] >= 0, name='')
            m.addConstr(x[r, b] - x[r-1, inverse_shuffle[b+1]] + x[r+1, shuffle[b+1]] >= 0, name='')
            m.addConstr(- x[r, b] + x[r-1, inverse_shuffle[b+1]] + x[r+1, shuffle[b+1]] >= 0, name='')

    m.setObjective(sum(x[r, i] for i in range(0, Branch)[::2] for r in range(1, Round))
                   + sum(x_in[0, i] for i in range(0, Branch)[::2]), GRB.MINIMIZE)
    # m.write('differential.lp')
    m.optimize()
    return int(m.Objval)


if __name__ == '__main__':
    # time_start = time.time()
    br_list = [4, 6, 8, 10, 12, 14, 16]
    for br in br_list:
        with open(r"ResultZCLinear/{}_branch_zc.pkl".format(br), 'rb') as f:
            SHUFFLES = pickle.load(f)
    #     SHUFFLES = {(7, 2, 13, 4, 15, 6, 1, 8, 5, 10, 3, 0, 11, 12, 9, 14) :  [8, 13, 15, 15] ,
    #                 (9, 2, 7, 4, 11, 6, 13, 8, 15, 10, 5, 0, 3, 12, 1, 14) :  [8, 13, 15, 15] ,
    #                 (5, 2, 9, 4, 15, 6, 13, 8, 3, 10, 7, 0, 11, 12, 1, 14) :  [8, 13, 15, 15] ,
    #                 (13, 2, 15, 4, 11, 6, 3, 8, 1, 10, 5, 0, 9, 12, 7, 14) :  [8, 13, 15, 15] ,
    #                 (5, 2, 9, 4, 13, 6, 15, 8, 3, 10, 7, 0, 1, 12, 11, 14) :  [8, 13, 15, 15] ,
    #                 (13, 2, 9, 4, 1, 6, 11, 8, 3, 10, 15, 0, 5, 12, 7, 14) :  [8, 13, 15, 15] ,
    #                 (15, 2, 9, 4, 1, 6, 11, 8, 3, 10, 13, 0, 7, 12, 5, 14) :  [8, 13, 15, 15] ,
    #                 (7, 2, 15, 4, 13, 6, 1, 8, 5, 10, 3, 0, 9, 12, 11, 14) :  [8, 13, 15, 15] ,
    #                 (15, 2, 13, 4, 11, 6, 3, 8, 1, 10, 5, 0, 7, 12, 9, 14) :  [8, 13, 15, 15] ,
    #                 (7, 2, 11, 4, 9, 6, 1, 8, 13, 10, 15, 0, 5, 12, 3, 14) :  [8, 13, 15, 15] ,
    #                 (7, 2, 11, 4, 9, 6, 1, 8, 15, 10, 13, 0, 3, 12, 5, 14) :  [8, 13, 15, 15] ,
    #                 (9, 2, 7, 4, 11, 6, 15, 8, 13, 10, 5, 0, 1, 12, 3, 14) :  [8, 13, 15, 15]}

        result = dict()
        border = [SHUFFLES.get(next(iter(SHUFFLES)))[0],
                  SHUFFLES.get(next(iter(SHUFFLES)))[1],
                  SHUFFLES.get(next(iter(SHUFFLES)))[2],
                  SHUFFLES.get(next(iter(SHUFFLES)))[3]]
        for sk, v in tqdm(SHUFFLES.items()):
            if all((abs(v[i] - border[i]) < 3) for i in range(4)):
                result[sk] = v + [generate_Differential_Model(sk)]

        tools.save_file(result, r'ResultDifferential/{}_branch_dc'.format(br), True)

        # for s in result:
        #     print(s, ': ', result[s], ',')
    # print(time.time() - time_start, '\n\n******\n Done \n******\n\n')
    # print(generate_Differential_Model((15, 4, 3, 0, 13, 6, 1, 2, 7, 12, 11, 8, 5, 14, 9, 10)))

