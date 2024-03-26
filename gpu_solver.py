import numpy as cp

# Phase I: Use a different representation of a position (bits instead of bytes)
    # Each tile is pair of 2 bits: 1 for empty(0) / taken(1), 1 for O(0) / X(1)

# Top-left tile is RIGHTmost bit pair; Read in levelorder, pad front with zeros
    # Number of tiles in position is M*N; A 5x3 board can fit inside 32-bit int

M, N, K = 2, 2, 2              # If >15 tiles: need int64

N_TIERS = M * N + 1            # Number of tiers w/ blank

BLANK_P = cp.int32(0b00)       # Blank board is all zeros

BITMASK = cp.int32(0b10)       # Get MSB pair with 0b..10

# Phase II: Pre-allocate memory upfront to avoid dynamic arrays for large tiers

def make_tiers():
    tier_arr = cp.zeros(N_TIERS, dtype=object)        # array of arrays (tiers)
    tier_arr[0] = cp.array([0x0], dtype=cp.int32)        # append a blank board

    for i in range(1, N_TIERS):                       # loop thru rest of tiers
        prev = tier_arr[i - 1]
        curr = cp.zeros(num_child(prev), dtype=cp.int32) # set curr tier's size

        populate(prev, curr, i)                       # curr == prev's children
        tier_arr[i] = curr                               # add all tiers to arr
    return tier_arr


def num_child(tier):
    count = 0
    for post in tier:                   # TODO: Fix nested loops.
        for _ in range(M * N):
            if (post & BITMASK) == 0:   # if left_bit == 0: empty
                count += 1
            post >>= 2                  # Shift to next tile/pair
    return count


def populate(prev, curr, tier_num):
    """
    King's notes:
    for p, i in enumerate(tier1):
        this_scratchpad = ai * 9 ~ (i+1) * 9 of scratchpad
            # go through each of 9 slots in scratchpad (or less than 9 children if at lower tiers)
            # copy position's current id into all 9 slots at first, then we make them into children
            # check if slot #i has a blank at tile #i, if so flip the bit so that it's now a piece
        id_position -> id_child1, id_child2, ...
    """
    index = 0
    flip_tile = 0b11 if (tier_num % 2) else 0b10
    # flip_tile = X  if (tier_num is odd) else O

    for post in prev:
        for i in range(M * N):
            if (post & (BITMASK << (i * 2))) == 0:

                new_post = post | (flip_tile << (i * 2))
                curr[index] = new_post
                index += 1


def print_board(post):
    chars = {0b00: ' ', 0b10: 'O', 0b11: 'X'}
    board = []
    
    for i in range(M * N):
        tile = (post >> (2 * (M * N - 1 - i))) & 0b11
        board.append(chars[tile])
    
    for i in range(M):
        print(' | '.join(board[i * N : (i+1) * N]))
        if i < M - 1:
            print('-' * (N * 4 - 3))

tier_arr = make_tiers()

for i in range(len(tier_arr)):
    print(f"\nTIER {i}:\n")

    for post in tier_arr[i]:
        print_board(post)
        print()

# TODO: implement deduplication with cuda/cupy library otherwise it's hella slow

"""
# Phase III: Solve the game. After a tier is finished, we can destroy the memory

tier_9_vals = new HashMap(size= foo(None))  # Make sizes of every HashMap fixed
tier_9_vals = solve_tier(tier_9, None)      # should not be dynamic for the GPU

tier_8_vals = new HashMap(size= foo(tier_8))
tier_8_vals = solve_tier(tier_9, tier_8_vals) # free tier_9 after tier_8 solved

# definitely look for a cupy library for making hashmaps, also for deduplication


# Hash Map
# https://developer.nvidia.com/blog/maximizing-performance-with-massively-parallel-hash-maps-on-gpus/


# Phase IV: Kernels. Example ElementwiseKernel

squared_diff = cp.ElementwiseKernel(
   'float32 x, float32 y',
   'float32 z',
   'z = (x - y) * (x - y)',
   'squared_diff')

x = cp.arange(10, dtype=np.float32).reshape(2, 5)
y = cp.arange(5,  dtype=np.float32)

print(squared_diff(x, y))
print(squared_diff(x, 5))

l2norm_kernel = cp.ReductionKernel(
    'T x',  # input params
    'T y',  # output params
    'x * x',  # map
    'a + b',  # reduce
    'y = sqrt(a)',  # post-reduction map
    '0',  # identity value
    'l2norm'  # kernel name
)
x = cp.arange(10, dtype=np.float32).reshape(2, 5)
print(l2norm_kernel(x, axis=1))
"""