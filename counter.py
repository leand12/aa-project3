import random
import math
import re
from abc import ABC, abstractmethod
from bloom_filter import BloomFilter


class Counter(ABC):

    def __init__(self, text_filename: str, stopwords_filename: str):
        self.filename = text_filename
        self.stopwords = set()
        with open(stopwords_filename, 'r') as fp:
            for word in fp:
                self.stopwords.add(word.strip())

    def read_words(self):
        with open(self.filename, 'r') as fp:
            for line in fp:
                # normalize words
                for word in line.split():
                    for n_word in re.sub(r'[^a-zA-Z]', ' ', word).split():
                        yield n_word.lower()
                
    @abstractmethod
    def count(self):
        pass


class ExactCounter(Counter):
    """Exact distinct word counter."""

    def __init__(self, text_filename: str, stopwords_filename: str):
        super().__init__(text_filename, stopwords_filename)

    def count(self):

        distinct_words = set()
        for word in self.read_words():
            distinct_words.add(word)
        return len(distinct_words)


class BloomFilterCounter(Counter):
    """Distinct word counter with bloom filter."""

    def __init__(self, text_filename: str, stopwords_filename: str, m: int, k: int):
        super().__init__(text_filename, stopwords_filename)
        self.filter = BloomFilter(m, k, hash)

    def count(self):

        distinct_words = 0
        for word in self.read_words():
            if not self.filter.contains(word):
                self.filter.insert(word)
                distinct_words += 1
        return distinct_words
