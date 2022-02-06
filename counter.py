import random
import math
from abc import ABC, abstractmethod
from bloom_filter import BloomFilter


class Counter(ABC):

    def __init__(self, filename: str):
        self.filename = filename

    def read_chars(self):
        with open(self.filename) as fp:
            for line in fp:
                # normalize words
                for word in line:
                    for n_word in re.sub(r'[^a-zA-Z0-9\'-]', ' ', term).split():
                        print(n_word)
                        yield n_word
                
    @abstractmethod
    def count(self):
        pass


class ExactCounter(Counter):
    """Exact distinct word counter."""

    def __init__(self, filename: str):
        super().__init__(filename)

    def count(self):

        return 0


class BloomFilterCounter(Counter):
    """Distinct word counter with bloom filter."""

    def __init__(self, filename: str):
        super().__init__(filename)

    def count(self):

        return 0
