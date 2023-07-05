

import gurobipy as gp
from gurobipy import GRB


def gen_DSMITM_model(ROUND, BRANCH, SHUFFLE):

    m = gp.Model('DS-MITM')
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

    # NO.ac_cells <= NO.(Key_length/size_cells) == we remove this constraint in ideal model==
    m.addConstr(sum(z[r, b] for b in range(int(BRANCH/2)) for r in range(ROUND)) <= BRANCH-1, name='')

    # obj function
    m.setObjective(sum(z[r, b] for b in range(int(BRANCH/2)) for r in range(ROUND)), GRB.MINIMIZE)
    # m.write('TWINE_DS-MITM_model.lp')
    return m

if __name__ == '__main__':

    SHUFFLET = [1, 4, 3, 0, 5, 2]
    # SHUFFLE_rev = [1, 2, 11, 6, 3, 0, 9, 4, 7, 10, 13, 14, 5, 8, 15, 12]

    degAB = -1
    for r_round in range(5, 99):
        b_branch = len(SHUFFLET)
        model = gen_DSMITM_model(r_round, b_branch, SHUFFLET)
        model.optimize()
        if model.Status == 2:
            degAB = model.Objval
        else:
            print('=====\n', r_round-1, 'is the longest DS-MITM_Dis round.', '\n=====')
            print('Deg =', degAB)
            break
        pass
