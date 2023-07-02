
import itertools
import multiprocessing
# import time
import numpy as np
from tqdm import tqdm
import numba as nb
from numba import jit

def rotate_left(lst, n):
    if len(lst) <= 1:
        return lst

    n %= len(lst)
    temp = lst[:n]
    for i in range(n, len(lst)):
        lst[i - n] = lst[i]

    lst[-n:] = temp
    return lst


def gen_new_cycle(cycle):
    new_cycle = [cycle + [1]]
    if len(cycle) == 1:
        new_cycle.append([cycle[0] + 1])
        return new_cycle
    if cycle[-1] < cycle[-2]:
        cycle[-1] += 1
        new_cycle.append(cycle)
    return new_cycle


def iterative_cycle(cur_cycle):
    new_cycles = []
    for cycle in cur_cycle:
        for c in gen_new_cycle(cycle):
            new_cycles.append(c)
    return new_cycles


def cycle_to_permutations(t_branch, cycles):
    disCycleClass = []
    for cycle in cycles:
        aConjugate = [i for i in range(t_branch)]
        i = 0
        result = []
        for r in cycle:
            j = i + r
            result += rotate_left(aConjugate[i:j], r - 1)
            i += r
        disCycleClass.append(result)

    disCycleClass = np.array(disCycleClass)
    return disCycleClass


def ConjugatedShufflesGeneration():
    temp_cycles = [[1]]
    b = 1
    while b < pair_ub:
        b += 1
        temp_cycles = iterative_cycle(temp_cycles)
        np.save(r'ConjugatedShuffles/{}_BranchConjugatedShuffles'.format(b), cycle_to_permutations(b, temp_cycles))


def InitialShufflesGeneration(b):
    perm = np.array(list(itertools.permutations(range(b))))
    np.save(r'InitialShuffles/{}_BranchInitialShuffles'.format(b), perm)
    return perm


@jit(nopython=True)
def ConditionalShufflesGeneration(initP, b):
    ConditionalPerms = nb.typed.List()
    for p in initP:
        conditionP = nb.typed.List([-1 for _ in range(2*b)])

        for i in range(b):
            conditionP[2 * i], conditionP[2 * i + 1] = 2 * p[i], 2 * p[i] + 1
        ConditionalPerms.append(conditionP)
    return ConditionalPerms


def check(pair_len):
    print('\nNumber of {}-branch initial permutations is'.format(pair_len),
          len(np.load(r'InitialShuffles/{}_BranchInitialShuffles.npy'.format(pair_len))))
    print('Number of {}-branch conjugated permutations is'.format(pair_len),
          np.load(r'ConjugatedShuffles/{}_BranchConjugatedShuffles.npy'.format(pair_len)))
    print('Number of {}-branch conditional permutations is'.format(2*pair_len),
          len(np.load(r'ConditionalShuffles/{}_BranchConditionalShuffles.npy'.format(2*pair_len))), '\n')


if __name__ == '__main__':
    # 2 to 8
    pair_lb = 2
    pair_ub = 8

    ConjugatedShufflesGeneration()

    for pr in range(pair_lb, pair_ub+1):

        perms = InitialShufflesGeneration(pr)

        tcp = np.array(ConditionalShufflesGeneration(perms, pr))

        np.save(r'ConditionalShuffles/{}_BranchConditionalShuffles'.format(2 * pr), np.array(tcp))

        check(pr)
