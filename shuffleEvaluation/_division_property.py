

import multiprocessing
import pickle
import gurobipy as gp
from gurobipy import GRB


class DivisionProperty:
    """
    Assume each branch have 4 bits for all 4, 6, 8,... branches, resp s-box
    And we consider only one input bit is 'inactive'
    """
    def __init__(self, ROUND, SHUFFLE, ACTIVE_BITS):
        self.round = ROUND
        self.shuffle = SHUFFLE
        self.branch = len(SHUFFLE)
        self.in_active_bits = ACTIVE_BITS
        self.total = self.branch * 4

    def gen_model(self):
        BRANCH = len(self.shuffle)
        m = gp.Model('division_property')
        x = m.addVars(self.round + 1, 4*BRANCH, vtype=GRB.BINARY, name='x')
        s = m.addVars(self.round, 4*BRANCH, vtype=GRB.BINARY, name='s')

        for r in range(self.round):
            # Copy
            for i in range(BRANCH)[::2]:
                for j in range(4):
                    m.addConstr(x[r, 4*i+j] - s[r, 4*i+j] - x[r+1, 4*self.shuffle[i]+j] == 0, name='')

            # S-box (These constraints for each s-box (never mind the branch))
            x_SB_ineq = [[1, 1, 1, 1, -1, -1, -1, -1, 0],
                         [0, 0, 0, 0, -1, -1, -1, 2, 1],
                         [0, 0, 0, 0, -1, -1, 2, -1, 1],
                         [-1, -1, -1, -1, 3, 3, 3, 3, 0],
                         [0, 0, 0, 0, -1, 2, -1, -1, 1],
                         [0, 0, 0, 0, 2, -1, -1, -1, 1]]
            sb_ineq = x_SB_ineq
            for i in range(int(BRANCH//2)):
                for ineq in sb_ineq:
                    m.addConstr(ineq[0] * s[r, 8*i] + ineq[1] * s[r, 8*i+1] +
                                ineq[2] * s[r, 8*i+2] + ineq[3] * s[r, 8*i+3] +
                                ineq[4] * s[r, 8*i+4] + ineq[5] * s[r, 8*i+5] +
                                ineq[6] * s[r, 8*i+6] + ineq[7] * s[r, 8*i+7] +
                                ineq[8] >= 0, name='')

            # Xor
            for i in range(1, BRANCH)[::2]:
                for j in range(4):
                    m.addConstr(x[r, 4*i+j] + s[r, 4*i+j] - x[r+1, 4*self.shuffle[i]+j] == 0, name='')

        # Active bits
        for i in range(self.in_active_bits, self.total)[::-1]:
            m.addConstr(x[0, i] == 1, name='')
        for i in range(self.in_active_bits):
            m.addConstr(x[0, i] == 0, name='')
        # m.addConstr(ALL_BITS-16 <= sum(x[0, i] for i in range(ALL_BITS)), name='')
        # m.addConstr(sum(x[0, i] for i in range(ALL_BITS)) <= ALL_BITS-1, name='')

        # Objective function
        m.setObjective(sum(x[self.round, i] for i in range(self.total)), GRB.MINIMIZE)

        # m.write('division_property.lp')
        return m

    def solve_model(self):
        model = self.gen_model()
        counter = 0
        zero_pos = []
        s_flag = False
        while counter < 64:
            model.optimize()
            if model.Status == 2:
                objfunc = model.getObjective()
                if objfunc.getValue() > 1:
                    # Find the distinguish_er
                    s_flag = True
                    break
                else:
                    # this position set to 0
                    for i in range(64):
                        u = objfunc.getVar(i)
                        temp = u.getAttr('x')
                        if temp == 1:
                            temp_pos = u.getAttr('VarName')
                            if temp_pos not in zero_pos:
                                zero_pos.append(temp_pos)
                            model.addConstr(u == 0, name='')
                            model.update()
                            counter += 1
                            break
            elif model.Status == 3:
                # INFEASIBLE ==> find the distinguish_er
                s_flag = True
                break
            else:
                break
        if len(zero_pos) == self.total:
            s_flag = False
        return s_flag

    @staticmethod
    def call_back(result):

        global varify_flag
        varify_flag.append(not result)

        if result:
            pool.terminate()


if __name__ == '__main__':

    br = 16
    shuffle_dict = {(9, 6, 13, 0, 11, 2, 15, 4, 3, 10, 7, 8, 1, 12, 5, 14) : [8, 44, 44, 15, 15, 12],
                    (1, 6, 7, 0, 9, 2, 15, 4, 5, 14, 3, 8, 13, 10, 11, 12) : [8, 44, 44, 15, 15, 12],
                    (1, 12, 9, 0, 5, 2, 15, 4, 11, 6, 3, 8, 7, 10, 13, 14) : [8, 44, 44, 16, 16, 12],
                    (1, 4, 13, 0, 7, 2, 9, 10, 3, 6, 15, 8, 11, 12, 5, 14) : [8, 44, 44, 16, 16, 12]
                    }

    global varify_flag
    for sk, v in shuffle_dict.items():
        r = 10
        while r < 50:
            varify_flag = []
            pool = multiprocessing.Pool(4)
            for ac in range(1, 16):
                dp = DivisionProperty(r, sk, ac, )
                pool.apply_async(dp.solve_model, args=(), callback=dp.call_back)
            pool.close()
            pool.join()

            if all(varify_flag):
                shuffle_dict[sk] = v + [r-1]
                break
            else:
                r += 1

    for sk, v in shuffle_dict.items():
        print(str(sk) + ': ' + str(v))
    print('\n\n====\n Done \n====\n\n')

    shuffle_dict = dict(sorted(shuffle_dict.items(), key=lambda key: (key[1][6])))
    with open('ResultIntegral/{}_branch.pkl'.format(br), 'wb') as fp:
        pickle.dump(shuffle_dict, fp)

    with open('ResultIntegral/{}_branch.txt'.format(br), 'w+') as f:
        for k, v in shuffle_dict.items():
            f.write(str(k) + ': ' + str(v) + '\n')




