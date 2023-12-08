import pickle
import multiprocessing
import time
import numpy as np
from shuffleEvaluation.tools import verify, save_file
from shuffleEvaluation._diffusion import rev


class Strategy:
    """
    all the permutations are saved as the binary pickle file for a faster IO
    The basic idea from readme.md -> Strategy.
    """
    def __init__(self, K, initial_p, conjugate_p, conditional_p):
        self.branch = K  # branch number of GFS
        self.pair = int(K / 2)  # number of Feistel
        self.temporaryPerm = [-1 for _ in range(self.branch)]  # permutation for temporary storing
        self.pairEquivalentPerms = set()  # target for searching
        self.initialPerms = initial_p
        self.conjugatePerms = conjugate_p
        self.conditionalPerms = conditional_p

    def filter(self):
        new_shuffles = set()
        for shuffle in self.pairEquivalentPerms:
            if verify(self.branch, shuffle, new_shuffles) or \
                    verify(self.branch, rev(shuffle), new_shuffles):
                pass
            else:
                new_shuffles.add(shuffle)
        print(self.branch, new_shuffles)
        return new_shuffles

    def judgeEquivalentClass(self, perm):
        for condition in self.conditionalPerms:

            # the inverse perm
            inverse_perm = self.temporaryPerm[:]
            for i, c in enumerate(condition):
                inverse_perm[c] = i

            # perm multiply
            judge_perm = self.temporaryPerm[:]
            for j in range(self.branch):
                judge_perm[j] = inverse_perm[perm[condition[j]]]

            # judge_perm = call(self.branch, condition, np.array(perm))
            # if one equivalent-class permutation in pairEquivalentPerms, abort
            if tuple(judge_perm) in self.pairEquivalentPerms:
                return False
        return True

    def pairEquivalentGeneration(self, sieve):
        for conjugate_perm in self.conjugatePerms:
            tempPerm = self.temporaryPerm[:]
            for initial_perm in self.initialPerms:
                for i, init in enumerate(initial_perm):
                    tempPerm[2 * i] = 2 * init + 1
                for j, conj in enumerate(conjugate_perm):
                    tempPerm[2 * j + 1] = 2 * conj
                if self.judgeEquivalentClass(tempPerm):
                    self.pairEquivalentPerms.add(tuple(tempPerm))

        self.pairEquivalentPerms = np.array([p for p in self.pairEquivalentPerms])
        print('\n=====\n' + str(self.branch) + ' branch --> No_perms = '
              + str(self.pairEquivalentPerms.size // self.branch) + '\n=====\n')
        np.save('PairEquivalentShuffles/{}_BranchPairEquivalentShuffles'.format(self.branch),
                np.array(self.pairEquivalentPerms))

    # def test(self):
    #     print(self.initialPerms, '\n', len(self.initialPerms))
    #     print(self.conjugatePerms, '\n', len(self.conjugatePerms))
    #     print(self.conditionalPerms, '\n', len(self.conditionalPerms))


if __name__ == '__main__':

    pool = multiprocessing.Pool(8)
    k_lis = [4, 6, 8, 10, 12, 14, 16]
    for k in k_lis:
        initialPerms = np.load('InitialShuffles/{}_BranchInitialShuffles.npy'.format(int(k/2)))
        conjugatePerms = np.load('ConjugatedShuffles/{}_BranchConjugatedShuffles.npy'.format(int(k/2)))
        conditionalPerms = np.load('ConditionalShuffles/{}_BranchConditionalShuffles.npy'.format(k))
        s = Strategy(k, initialPerms, conjugatePerms, conditionalPerms)
        # s.pairEquivalentGeneration(False)
        pool.apply_async(s.pairEquivalentGeneration, args=(False, ))
    pool.close()
    pool.join()
