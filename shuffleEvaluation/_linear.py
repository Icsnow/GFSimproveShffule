

import gurobipy as gp
from gurobipy import GRB


def generate_Linear_Model(permutation):
    """
    Note: the permutation are all eo-permutation,so for all b is even positions
    x[r,b+1] from the last round (without constraints)
    """
    Round = 20
    Branch = len(permutation)
    inverse_permutation = [permutation.index(i) for i in range(Branch)]

    # Variables
    m = gp.Model('Truncated Linear Evaluation')
    # iniRound = [(0, b) for b in range(0, Branch)[::2]]
    x_in = m.addVars(1, Branch, vtype=GRB.BINARY, name='x0')
    midRound = [(r, b) for b in range(1, Branch)[::2] for r in range(1, Round+1)]
    x = m.addVars(midRound, vtype=GRB.BINARY, name='x')

    # Initial constraint
    m.addConstr(sum(x_in[0, i] for i in range(Branch)) >= 1, name='')

    # XOR constraint
    for b in range(1, Branch)[::2]:
        m.addConstr(x_in[0, b] + x_in[0, b-1] - x[1, permutation[b-1]] >= 0, name='')
        m.addConstr(x_in[0, b] - x_in[0, b-1] + x[1, permutation[b-1]] >= 0, name='')
        m.addConstr(- x_in[0, b] + x_in[0, b-1] + x[1, permutation[b-1]] >= 0, name='')

        m.addConstr(x[1, b] + x_in[0, inverse_permutation[b-1]] - x[2, permutation[b-1]] >= 0, name='')
        m.addConstr(x[1, b] - x_in[0, inverse_permutation[b-1]] + x[2, permutation[b-1]] >= 0, name='')
        m.addConstr(- x[1, b] + x_in[0, inverse_permutation[b-1]] + x[2, permutation[b-1]] >= 0, name='')

    for r in range(2, Round):
        for b in range(1, Branch)[::2]:
            m.addConstr(x[r, b] + x[r-1, inverse_permutation[b-1]] - x[r+1, permutation[b-1]] >= 0, name='')
            m.addConstr(x[r, b] - x[r-1, inverse_permutation[b-1]] + x[r+1, permutation[b-1]] >= 0, name='')
            m.addConstr(- x[r, b] + x[r-1, inverse_permutation[b-1]] + x[r+1, permutation[b-1]] >= 0, name='')

    m.setObjective(sum(x[r, i] for i in range(1, Branch)[::2] for r in range(1, Round))
                   + sum(x_in[0, i] for i in range(1, Branch)[::2]), GRB.MINIMIZE)
    # m.write('linear.lp')
    m.optimize()
    return m.Objval
