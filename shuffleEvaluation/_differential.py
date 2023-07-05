

import gurobipy as gp
from gurobipy import GRB


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
    return m.Objval


# generate_Differential_Model([1, 0, 3, 2])