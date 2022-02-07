import matplotlib.pyplot as plt
import numpy as np
from bloom_filter import BloomFilter
from counter import BloomFilterCounter, ExactCounter


def test_optimal_values():
    sizes = []
    hashes = []
    probs = np.arange(0.01, 0.5, 0.02)
    for prob in probs:
        m = BloomFilter.get_bitarray_size(12566, prob)
        k = BloomFilter.get_hash_count(m, 12566)
        sizes.append(m)
        hashes.append(k)

    fig, ax = plt.subplots()

    twin1 = ax.twinx()

    p1, = ax.plot(probs, sizes, "b-", label="Bit Array Size")
    p2, = twin1.plot(probs, hashes, "r-", label="Number of Hashes")

    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, max(sizes))
    twin1.set_ylim(0, max(hashes))

    ax.set_xlabel("False Positive Probability")
    ax.set_ylabel("Bit Array Size")
    twin1.set_ylabel("Number of Hashes")

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())

    tkw = dict(size=4, width=1.5)
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
    twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    ax.tick_params(axis='x', **tkw)

    ax.legend(handles=[p1, p2])

    plt.show()


def test_cbf_hashes():

    exact = ExactCounter('texts/english.txt', 'stopwords/english.txt').count()

    counts = []
    for k in range(1, 20):
        counter = BloomFilterCounter('texts/english.txt', 'stopwords/english.txt',  60000, k)
        counts.append(1 - counter.count() / exact)

    plt.plot(range(1, 20), counts)
    plt.xticks(range(1, 20))
    plt.xlabel("Number of Hashes")
    plt.ylabel("False Positive Rate")
    plt.show()


def test_cbf_sizes():

    exact = ExactCounter('texts/english.txt', 'stopwords/english.txt').count()

    counts = []
    for m in range(1000, 120000, 5000):
        counter = BloomFilterCounter('texts/english.txt', 'stopwords/english.txt', m, 5)
        counts.append(1 - counter.count() / exact)

    plt.plot(range(1000, 120000, 5000), counts)
    plt.xlim(0, 120000)
    plt.xlabel("Bit Array Size")
    plt.ylabel("False Positive Rate")
    plt.show()
