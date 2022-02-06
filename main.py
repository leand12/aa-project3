import argparse
from bloom_filter import BloomFilter
from counter import ExactCounter, BloomFilterCounter


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Distinct Word Counting Program')

    parser.add_argument('text-file', type=argparse.FileType('r'),
                        help='the path of the file with the words to be counted')
    parser.add_argument('stopwords-file', type=argparse.FileType('r'),
                        help='the path of the file with the words that should be ignored')

    subparser = parser.add_subparsers(
        title='counter type', dest='counter-type', required=True, help='type of the counter')

    exact_parser = subparser.add_parser('exact',
                                        help='run with an exact counter')
    bloom_parser = subparser.add_parser('bloom',
                                        help='run with a counter based on bloom filter')

    bloom_parser.add_argument('-t', '--test', action='store_true',
                              help='test results comparing with exact counter')

    bloom_subparser = bloom_parser.add_subparsers(
        title='bloom type', dest='bloom-type', required=True, help='type of the counter')

    bloom_parser_custom = bloom_subparser.add_parser('custom',
                                                     help='bloom parser with custom configurations')
    bloom_parser_custom.add_argument('-m', '--size', metavar='SIZE', default=5000, type=int,
                                     help='size of the bitarray used by bloom filter (default: %(default)s)')
    bloom_parser_custom.add_argument('-k', '--hashes', metavar='NUM', default=5, type=int,
                                     help='number of hashes used by bloom filter (default: %(default)s)')

    bloom_parser_optimal = bloom_subparser.add_parser('optimal',
                                                      help='bloom parser with optimal configurations')
    bloom_parser_optimal.add_argument('-n', '--expected', metavar='NUM', default=1000, type=int,
                                      help='expected number of keys to be stored (default: %(default)s)')
    bloom_parser_optimal.add_argument('-p', '--false-positive', metavar='PROB', default=0.1, type=float,
                                      help='probability of having a false positive (default: %(default)s)')

    args = parser.parse_args()
    vargs = vars(args)

    # m = BloomFilter.get_bitarray_size(n, p)
    # k = BloomFilter.get_hash_count(m, n)

    if vargs['counter-type'] == 'exact':
        counter = ExactCounter(
            vargs['text-file'].name, vargs['stopwords-file'].name)
    else:
        if vargs['bloom-type'] == 'custom':
            m = args.size
            k = args.hashes
        else:
            m = BloomFilter.get_bitarray_size(args.expected, args.false_positive)
            k = BloomFilter.get_hash_count(m, args.expected)

        counter = BloomFilterCounter(
            vargs['text-file'].name, vargs['stopwords-file'].name, m, k)

    print(counter.count())
