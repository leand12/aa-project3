import argparse
from bloom_filter import BloomFilter
from counter import ExactCounter, BloomFilterCounter
from test import test_optimal_values, test_cbf_hashes, test_cbf_sizes


def check_probability(value):
    ivalue = float(value)
    if not 0 < ivalue <= 1:
        raise argparse.ArgumentTypeError("%s is an invalid probability" % value)
    return ivalue


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
        title='bloom type', dest='bloom-type', required=False, help='type of the counter')

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
    bloom_parser_optimal.add_argument('-p', '--false-positive', metavar='PROB', default=0.1, type=check_probability,
                                      help='probability of having a false positive (default: %(default)s)')

    args = parser.parse_args()
    vargs = vars(args)

    if vargs['counter-type'] == 'exact':
        print(f"Running Exact Counter...")
        counter = ExactCounter(
            vargs['text-file'].name, vargs['stopwords-file'].name)
    else:
        if args.test:
            test_optimal_values()
            test_cbf_sizes()
            test_cbf_hashes()
            exit(0)
        else:
            if vargs['bloom-type'] == 'custom':
                m = args.size
                k = args.hashes
            else:
                m = BloomFilter.get_bitarray_size(args.expected, args.false_positive)
                k = BloomFilter.get_hash_count(m, args.expected)

            print(f"Running Bloom Filter Counter with m={m} and k={k}...")
            counter = BloomFilterCounter(
                vargs['text-file'].name, vargs['stopwords-file'].name, m, k)

    print("%d distinct words counted" % counter.count())
