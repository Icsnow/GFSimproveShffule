

def cycleDecompose(permutation):
    pos = 0
    deg = 1
    while True:
        # print(pos, end=',')
        pos = permutation[pos]
        if pos != 0:
            deg += 1
        else:
            break
    if deg == len(permutation):
        print(permutation)
    # print(deg)

# PERMS14 = [(3, 4, 11, 0, 7, 2, 5, 8, 13, 6, 9, 10, 1, 12),
# (1, 6, 5, 0, 13, 2, 9, 4, 3, 10, 7, 8, 11, 12),
# (1, 6, 9, 0, 7, 2, 11, 4, 13, 10, 3, 8, 5, 12),
# (1, 4, 7, 0, 11, 2, 9, 10, 3, 6, 13, 8, 5, 12),
# (1, 4, 13, 0, 7, 2, 9, 10, 5, 6, 3, 8, 11, 12),
# (3, 8, 11, 0, 13, 2, 1, 4, 5, 6, 9, 10, 7, 12),
# (1, 12, 11, 0, 7, 2, 13, 4, 9, 6, 5, 8, 3, 10),
# (3, 8, 7, 0, 11, 2, 13, 4, 5, 6, 1, 10, 9, 12),
# (3, 8, 7, 0, 11, 2, 9, 4, 13, 6, 5, 12, 1, 10),
# (1, 12, 5, 0, 13, 2, 11, 4, 9, 6, 3, 8, 7, 10),
# (1, 6, 7, 0, 9, 2, 13, 4, 3, 12, 11, 8, 5, 10),
# (3, 8, 7, 0, 11, 2, 9, 4, 13, 6, 1, 10, 5, 12),
# (1, 8, 5, 0, 11, 2, 7, 4, 13, 6, 3, 12, 9, 10),
# (3, 8, 11, 0, 9, 2, 13, 4, 5, 6, 7, 10, 1, 12),
# (1, 6, 9, 0, 13, 2, 3, 4, 5, 12, 11, 8, 7, 10),
# (5, 6, 9, 0, 11, 2, 13, 4, 7, 8, 1, 10, 3, 12),
# (5, 8, 9, 0, 11, 2, 3, 4, 13, 6, 1, 10, 7, 12),
# (1, 6, 7, 0, 9, 2, 13, 4, 11, 12, 5, 8, 3, 10),
# (3, 12, 7, 0, 1, 2, 13, 4, 11, 6, 5, 8, 9, 10),
# (3, 12, 13, 0, 9, 2, 1, 4, 11, 6, 7, 8, 5, 10),
# (3, 10, 11, 0, 9, 2, 1, 4, 13, 6, 7, 8, 5, 12),
# (3, 10, 11, 0, 9, 2, 1, 4, 5, 6, 13, 8, 7, 12),
# (1, 10, 5, 0, 9, 2, 3, 4, 11, 6, 13, 8, 7, 12),
# (3, 10, 9, 0, 1, 2, 11, 4, 5, 6, 13, 8, 7, 12),
# (1, 10, 5, 0, 9, 2, 13, 4, 11, 6, 7, 8, 3, 12),
# (3, 10, 9, 0, 1, 2, 11, 4, 13, 6, 7, 8, 5, 12),
# (3, 8, 11, 0, 9, 2, 13, 4, 5, 6, 1, 10, 7, 12),
# (1, 8, 9, 0, 7, 2, 11, 4, 3, 6, 5, 12, 13, 10),
# (1, 6, 9, 0, 5, 2, 11, 4, 7, 12, 13, 8, 3, 10)]


PERMS4 = [(3, 0, 1, 2),
          (1, 2, 3, 0)]

PERMS6 = [(1, 2, 5, 0, 3, 4)]

PERMS8 = [(5, 2, 7, 0, 1, 4, 3, 6),
          (1, 2, 5, 0, 3, 6, 7, 4)]

PERMS10 = [(1, 6, 5, 0, 9, 2, 3, 4, 7, 8),
           (1, 6, 9, 0, 7, 2, 3, 4, 5, 8),
           (3, 4, 7, 0, 9, 2, 1, 6, 5, 8),
           (1, 4, 5, 0, 7, 2, 3, 8, 9, 6),
           (1, 2, 5, 0, 3, 6, 9, 4, 7, 8)]

PERMS12 = [(1, 2, 5, 0, 3, 6, 9, 4, 7, 10, 11, 8),
           (1, 4, 5, 0, 7, 2, 3, 8, 11, 6, 9, 10),
           (5, 2, 9, 0, 1, 6, 11, 4, 3, 8, 7, 10),
           (1, 6, 9, 0, 7, 2, 3, 4, 5, 10, 11, 8),
           (3, 4, 7, 0, 11, 2, 1, 8, 9, 6, 5, 10),
           (3, 4, 11, 0, 7, 2, 5, 8, 9, 6, 1, 10)]

PERMS14 = [(1, 4, 7, 0, 11, 2, 9, 10, 3, 6, 13, 8, 5, 12),
           (1, 4, 13, 0, 7, 2, 9, 10, 5, 6, 3, 8, 11, 12)]

PERMS16 = [(1, 4, 13, 0, 7, 2, 9, 10, 3, 6, 15, 8, 11, 12, 5, 14),
           (1, 12, 9, 0, 5, 2, 15, 4, 11, 6, 3, 8, 7, 10, 13, 14)]

for p in PERMS16:
    cycleDecompose(p)