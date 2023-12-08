

import tools
import numpy as np
from shuffleEvaluation._diffusion import rev
from tqdm import tqdm


def ex_filter(br):
    t_shuffle = np.load(r'../shuffleGeneration/PairEquivalentShuffles/{}_BranchPairEquivalentShuffles.npy'.format(br))

    shuffles = [tuple(s) for s in t_shuffle]

    new_shuffle = set()

    for s in tqdm(shuffles):
        if tools.verify(br, s, new_shuffle) or tools.verify(br, rev(s), new_shuffle):
            pass
        else:
            new_shuffle.add(s)

    res = np.array([p for p in new_shuffle])
    np.save(f'PairEquivalentShuffles/{br}_BranchPairEquivalentShuffles_filtered',
            np.array(res))
    with open(f'PairEquivalentShuffles/{br}_BranchPairEquivalentShuffles_filtered.txt', 'w+') as f:
        for ts in res:
            f.write(str(ts) + '\n')
    print(f'branch {br} No.shuffle is {len(new_shuffle)}')


if __name__ == '__main__':
    ex_filter(16)