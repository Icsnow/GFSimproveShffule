

import numpy as np

for br in [4, 6, 8, 10, 12, 14, 16]:
    X = np.load(r"C:\Users\Snow\Nutstore\1\Improve_Shuffle_in_GFS\DrawingPaper\FileUpdate\GFSimproveShffule\shuffleGeneration\PairEquivalentShuffles\{}_BranchPairEquivalentShuffles.npy".format(br))
    with open(r"C:\Users\Snow\Nutstore\1\Improve_Shuffle_in_GFS\DrawingPaper\FileUpdate\GFSimproveShffule\shuffleGeneration\PairEquivalentShuffles\{}_BranchPairEquivalentShuffles.txt".format(br), 'w') as f:
        for x in X:
            f.write(str(x) + '\n')
