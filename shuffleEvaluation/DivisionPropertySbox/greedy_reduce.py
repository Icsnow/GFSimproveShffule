

import re

class GreedyReduceInequalities:

    def __init__(self, ineqFileName, trailsFileName, NumberParametersIN, NumberParameterOUT):
        self.ineqFileName = ineqFileName
        self.trailsFileName = trailsFileName
        self.n_parameters_in = NumberParametersIN
        self.n_parameters_out = NumberParameterOUT
        self.v_presentation = self.analysesInequality()
        self.impossibleTrails = self.generateImpossible()

    def analysesInequality(self):
        """
        Fino
        Calls sageMath to generate inequalities through trails, parsing them into code-readable format
        """
        V_presentation = []
        with open(self.ineqFileName, 'r') as f:
            line = f.readline().replace(' ','')
            while line:
                temp_v = [int(s) for s in re.findall('-?\d+\.*\d*', line)][:-1]
                V_presentation.append(temp_v)
                line = f.readline().replace(' ','')
        return V_presentation

    def generateImpossible(self):
        """
        Amantillado
        Generate all possible trails, eliminate available, and leave the impossible
        """
        trails = []
        with open(self.trailsFileName, 'r') as f:
            line = f.readline()
            while line:
                temp_t = [int(s) for s in re.findall(r"-?\d+", line)]
                trails.append(temp_t)
                line = f.readline()

        all_trail = []
        for i in range(2**self.n_parameters_in):
            temp_in = list(bin(i)[2:].zfill(self.n_parameters_in))
            for o in range(2**self.n_parameters_out):
                temp_out = list(bin(o)[2:].zfill(self.n_parameters_out))
                all_trail.append([int(t) for t in (temp_in + temp_out)])

        for t in trails:
            if t in all_trail:
                all_trail.remove(t)
        return all_trail

    def verify_inequalities(self, ineq, trail):
        """
        Muscadet
        whether trail match the inequality or not ?
        """
        arrow = 0
        for i in range(self.n_parameters_in + self.n_parameters_out):
            arrow += ineq[i] * trail[i]
        arrow += ineq[-1]
        return True if arrow >= 0 else False

    def miss_count(self, ineq, impossible_trails):
        """
        Sancerre
        how many trail can be rule out by the inequality
        """
        counter = 0
        hits = []
        for it in impossible_trails:
            if not self.verify_inequalities(ineq, it):
                counter += 1
                hits.append(it)
        return counter, hits

    def greedy(self):
        """
        Main course
        save the top miss hit and remove the hits trails (greedy)
        """
        current_inequalities = self.v_presentation
        current_impossible_trails = self.impossibleTrails
        save_inequality = []
        while True:
            temp_inequality = []
            max_trails = []
            max_hits = 0
            for ineq in current_inequalities:
                temp_hits, temp_trails = self.miss_count(ineq, current_impossible_trails)
                if temp_hits > max_hits:
                    max_hits = temp_hits
                    temp_inequality = ineq
                    max_trails = temp_trails
            if temp_inequality in current_inequalities:
                current_inequalities.remove(temp_inequality)
            if temp_inequality not in save_inequality:
                save_inequality.append(temp_inequality)

            for rm in max_trails:
                current_impossible_trails.remove(rm)
            if not current_impossible_trails:
                break
            # print(len(current_impossible_trails), current_impossible_trails)

        print('\nDone, the number of reduced inequalities is: ', len(save_inequality))
        with open('reduced_inequalities.txt', 'w') as f:
            for ineq in save_inequality:
                f.write(str(ineq) + '\n')


if __name__ == '__main__':

    Hp = 'inequalities.txt'
    paths = 'availableTrails.txt'
    n_p_in = 4
    n_p_out = 4
    Method = GreedyReduceInequalities(Hp, paths, n_p_in, n_p_out)

    Method.greedy()