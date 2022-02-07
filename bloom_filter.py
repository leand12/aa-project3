import math
from typing import Callable


class BitArray:

    def __init__(self, size: int):
        self.size = size
        self.array = 0

    def set_bit(self, bit: int, value: bool):
        assert 0 <= bit < self.size
        self.array &= ~(1 << bit)
        self.array |= value << bit

    def get_bit(self, bit: int):
        assert 0 <= bit < self.size
        return self.array & (1 << bit)


class BloomFilter:
    """
    Bloom Filter

    @param m: size of the bitarray
    @param k: number of hash functions to compute
    @param hash_fun: hash function to use
    """

    def __init__(self, m: int, k: int, hash_fun: Callable[[str], int]):
        self.m = m
        self.k = k
        self.hash_fun = hash_fun

        self.vector = BitArray(self.m)

    @classmethod
    def get_bitarray_size(self, n: int, p: float):
        """
        Return the size of the bit array to be used for
        a predefined false positive rate

        @param n: number of items expected to be stored
        @param p: false positive probability
        """
        m = -(n * math.log(p))/(math.log(2)**2)
        return round(m)

    @classmethod
    def get_hash_count(self, m: int, n):
        """
        Return the ideal number of hash function to be used

        @param m: size of bit array
        @param n: number of items expected to be stored
        """
        k = (m/n) * math.log(2)
        return round(k)

    def insert(self, key):
        """ Insert a key """

        for i in range(self.k):
            bit = self.hash_fun(key + str(i)) % self.m
            self.vector.set_bit(bit, True)

    def contains(self, key):
        """ Check if key is contained """

        for i in range(self.k):
            bit = self.hash_fun(key + str(i)) % self.m
            if not self.vector.get_bit(bit):
                return False    # the key doesn't exist

        return True             # the key can be in the data set
