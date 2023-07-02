# Title

**/\* Author: Snow (2023.6.18) \*/

## These algorithms for generating the permutations

The algorithm from [2019]

* Method 'InitialPermutationsGeneration': generating initial permutations, say S_p in paper.

* Method 'ConjugatedPermutationsGeneration': Iterative calculating the distinct cycle decompositions of
  permutations of S_p, generating the one permutation of the conjugate-class.

  > Example:
  > branch = 2;
  > distinct cycle decompositions of permutations = [[1, 1], [2]];
  > the corresponding permutation are [0, 1] and [1, 0] which length of cycle decompositions are (1,1) and (2);
  > calculate the next situation (branch = 3) by 'gen_new_cycle';
  > iterate this process.
* Method 'ConditionalPermutationsGeneration': calling the initial permutations to generate conditional permutations, say S_p^k in paper.
