import numpy as cp
import gpu_objects as gpu

# Phase I: Use a different representation of a position (bits instead of bytes)
    # Each tile is pair of 2 bits: 1 for empty(0) / taken(1), 1 for O(0) / X(1)

# Top-left tile is RIGHTmost bit pair; Read in levelorder, pad front with zeros
    # Number of tiles in position is M*N; A 4x4 board can fit inside 32-bit int

M, N, K = 2, 2, 2           # If >16 tiles: need int64
N_TIERS = M * N + 1         # Number of tiers w/ blank

BLANK_P = cp.uint32(0b00)   # Blank board is all zeros
BITMASK = cp.uint32(0b10)   # Get MSB pair with 0b..10

X = cp.uint8(0b11)          # Store X and O in uint8's
O = cp.uint8(0b10)          # DO NOT BITMASK W/ THESE!

# Phase II: Pre-allocate memory upfront to avoid dynamic arrays for large tiers

def make_tiers():
    tier_arr = cp.empty(N_TIERS, dtype=object)        # array of arrays (tiers)
    tier_arr[0] = cp.array([BLANK_P], dtype=cp.uint32)   # append a blank board

    for i in range(1, N_TIERS):                       # loop thru rest of tiers
        prev = tier_arr[i - 1]                           # set curr tier's size
        curr = cp.empty(num_child(prev), dtype=cp.uint32)

        fill_tier(prev, curr, i)                       # curr == prev's children
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


def fill_tier(prev, curr, tier_num):
    """
    for p, i in enumerate(tier1):
        this_scratchpad = ai * 9 ~ (i+1) * 9 of scratchpad
            # go through each of 9 slots in scratchpad (or less than 9 children if at lower tiers)
            # copy position's current id into all 9 slots at first then we make them into children
            # check if slot #i has a blank at tile #i, if so flip the bit so that it's now a piece
        id_position -> id_child1, id_child2, ...
    """
    index = 0
    flip_tile = X if (tier_num % 2) else O

    for post in prev:
        for i in range(M * N):
            if (post & (BITMASK << (i * 2))) == 0:

                new_post = post | (flip_tile << (i * 2))
                curr[index] = new_post
                index += 1


def print_tiers():
    """
    Debug function to print result. Don't ask don't tell I forgot how it works
    """
    chars = {BLANK_P: " ", O: "O", X: "X"}
    tier_arr = make_tiers()

    for i in range(len(tier_arr)):
        print(f"\nTIER {i}:\n")

        for post in tier_arr[i]:
            board = []; print()

            for i in range(M * N):
                tile = (post >> (2 * (M * N - 1 - i))) & 0b11
                board.append(chars[tile])
        
            for i in range(M):
                print(" | ".join(board[i * N : (i+1) * N]))
                if i < M - 1:
                    print("-" * (N * 4 - 3))

"""
Phase III: Solve the game. After a tier is finished, we can destroy the memory.

tier_9_vals = new HashMap(size= foo(None))  # Make sizes of every HashMap fixed
tier_9_vals = solve_tier(tier_9, None)      # should not be dynamic for the GPU

tier_8_vals = new HashMap(size= foo(tier_8))
tier_8_vals = solve_tier(tier_9, tier_8_vals) # free tier_9 after tier_8 solved

TODO: implement deduplication with cuda/cupy library otherwise it's hella slow.

https://developer.nvidia.com/blog/maximizing-performance-with-massively-parallel-hash-maps-on-gpus/
"""

WIN = cp.uint8(0b00)
LOSE= cp.uint8(0b01)
TIE = cp.uint8(0b10)

# TODO: see gpu_objects.py
cupy_hashmap  = gpu.CupyHashMap (size=None)
numba_hashmap = gpu.NumbaHashMap(size=None)


def primitive_value(post):
    """
    TODO: This function is straight copied from homefun LMFAO have fun testing
    """
    def to_grid(post):
        grid = cp.empty(M * N, dtype=cp.uint8)  # Turn bitwise post to arr

        for i in range(M * N):
            grid[i] = (post >> (2 * i)) & 0b11  # Extract each bitstr pair
        return grid

    def has_end(line):
        x, o = 0, 0             # Counter variables of X/O
        for tile in line:

            if   tile == X:     x, o = x + 1, 0
            elif tile == O:     x, o = 0, o + 1
            else:               x, o = 0, 0
                
            if x >= K or o >= K:
                return True
        return False
    
    grid = to_grid(post)

    for i in range(M):          # rows
        if has_end(grid[i, :]):
            return LOSE
    for j in range(N):          # cols
        if has_end(grid[:, j]):
            return LOSE

    for d in range(-M + K, N - K + 1):  # y = -x
        if has_end(grid.diagonal(d)):
            return LOSE                 # y = +x
        if has_end(cp.fliplr(grid).diagonal(d)):
            return LOSE

    if BLANK_P not in grid:     # no empty tiles
        return TIE

if __name__ == "__main__":
    print_tiers()

"""
# Phase IV: Kernels

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