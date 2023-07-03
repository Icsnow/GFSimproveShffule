

import gurobipy as gp
from gurobipy import GRB
import re
import multiprocessing

def shuffle(pos):
    p = [5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14]
    return p[pos]

def gen_divisionProperty_model(ROUND, ACTIVE_BITS):

    m = gp.Model('TWINE_division_property')
    x = m.addVars(ROUND + 1, 64, vtype=GRB.BINARY, name='x')
    s = m.addVars(ROUND, 64, vtype=GRB.BINARY, name='s')

    for rp in range(ROUND):
        # Copy
        for i in range(16)[::2]:
            for j in range(4):
                m.addConstr(x[rp, 4 * i + j] - s[rp, 4 * i + j] - x[rp + 1, 4 * shuffle(i) + j] == 0)

        # S-box
        x_SB_ineq = [[1, 1, 1, 1, -1, -1, -1, -1, 0],
                     [0, 0, 0, 0, -1, -1, -1, 2, 1],
                     [0, 0, 0, 0, -1, -1, 2, -1, 1],
                     [-1, -1, -1, -1, 3, 3, 3, 3, 0],
                     [0, 0, 0, 0, -1, 2, -1, -1, 1],
                     [0, 0, 0, 0, 2, -1, -1, -1, 1]]
        sb_ineq = x_SB_ineq
        for i in range(8):
            for ineq in sb_ineq:
                m.addConstr(ineq[0] * s[rp, 8 * i] + ineq[1] * s[rp, 8 * i + 1] +
                            ineq[2] * s[rp, 8 * i + 2] + ineq[3] * s[rp, 8 * i + 3] +
                            ineq[4] * s[rp, 8 * i + 4] + ineq[5] * s[rp, 8 * i + 5] +
                            ineq[6] * s[rp, 8 * i + 6] + ineq[7] * s[rp, 8 * i + 7] +
                            ineq[8] >= 0, name='')

        # Xor
        for i in range(1, 16)[::2]:
            for j in range(4):
                m.addConstr(x[rp, 4 * i + j] + s[rp, 4 * i + j] - x[rp + 1, 4 * shuffle(i) + j] == 0, name='')

    # Active bits
    for i in range(64-ACTIVE_BITS, 64)[::-1]:
        m.addConstr(x[0, i] == 1, name='')
    for j in range(0, 64-ACTIVE_BITS):
        m.addConstr(x[0, j] == 0, name='')

    # Objective function
    m.setObjective(sum(x[ROUND, i] for i in range(64)), GRB.MINIMIZE)

    m.write('TWINE.lp')
    return m

def solve_divisionProperty_model(RRound, Active_bits):
    model = gen_divisionProperty_model(RRound, Active_bits)
    counter = 0
    zero_pos = []
    s_flag = False
    while counter < 64:
        model.optimize()
        if model.Status == 2:
            objfunc = model.getObjective()
            if objfunc.getValue() > 1:
                # Find distinguish_er
                s_flag = True
                break
            else:
                for i in range(64):
                    u = objfunc.getVar(i)
                    temp = u.getAttr('x')
                    if temp == 1:
                        temp_pos = u.getAttr('VarName')
                        if temp_pos not in zero_pos:
                            zero_pos.append(temp_pos)
                        model.addConstr(u == 0)
                        model.update()
                        counter += 1
                        break
        elif model.Status == 3:
            # INFEASIBLE
            s_flag = True
            break
        else:
            break
    if len(zero_pos) == 64:
        s_flag = False
    if s_flag:
        with open('zero_position_' + str(RRound) + 'r.txt', 'w') as fz:
            for z in zero_pos:
                fz.write(str(z) + '\n')
            fz.write('\n number of activate: ' + str(Active_bits) + '\n')
    return not s_flag


def call_back(result):

    global varify_flag
    varify_flag.append(result)

    if not result:
        pool.terminate()


if __name__ == '__main__':

    global varify_flag
    r_main = 10
    while r_main < 30:
        varify_flag = []
        pool = multiprocessing.Pool(16)
        for acb in range(48, 64):
            pool.apply_async(solve_divisionProperty_model, args=(r_main, acb, ), callback=call_back)
        pool.close()
        pool.join()

        if all(varify_flag):
            print('\n\n========\n find ' + str(r_main-1) + '-round integral_distinguish_er!!\n========\n\n')
            break
        else:
            r_main += 1
