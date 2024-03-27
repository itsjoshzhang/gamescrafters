import numpy as cp
from numba import cuda

BLANK_P = cp.uint32(0b00)                           # Blank board is all zeros
pow_2 = lambda size: 2 ** (size - 1).bit_length()   # Ensure size = power of 2

key32 = lambda size: cp.zeros(size, dtype=cp.int32) # Positions are 32-bit int
vals8 = lambda size: cp.zeros(size, dtype=cp.int8)  # Values (W,L,T) are 8-bit

def check_key(key):
    if not isinstance(key, cp.uint32) or key == BLANK_P:
        raise ValueError("Bad input position to hashmap")

class CupyHashMap:

    def __init__(self, size):
        size = pow_2(size)
        self.mask = size - 1    # For bitwise hash fn. idk

        self.keys = key32(size)  
        self.vals = vals8(size)

    def hash(self, key):
        return key & self.mask  # TODO: find better hash fn

    def insert(self, key, val):
        check_key(key)
        i = self.hash(key)
        
        while self.keys[i] != BLANK_P:  # Linear probing for array
            if self.keys[i] == key:     # Don't add duplicate keys
                return
            
            i = (i + 1) & self.mask     # Index is full so move on
        self.keys[i] = key              # Loop is over, now insert
        self.vals[i] = val


@cuda.jit
def insert_kernel(keys, vals, size, mask, key, val):
    i = cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x

    if i < size:
        hashed = key & mask
        while True:
            if keys[hashed] == BLANK_P or keys[hashed] == key:
                keys[hashed] = key
                vals[hashed] = val
                break
            hashed = (hashed + 1) & mask

class NumbaHashMap:
    def __init__(self, size):
        size = pow_2(size)
        self.mask = size - 1    # For bitwise hash fn. idk

        self.keys = key32(size)  
        self.vals = vals8(size)

    