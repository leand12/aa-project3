import argparse
from counter import ExactCounter, BloomFilterCounter


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Distinct Word Counting Program')

    parser.add_argument('text-file', type=argparse.FileType('r'),
                        help='the path of the file with the words to be counted')
    parser.add_argument('stopwords-file', type=argparse.FileType('r'),
                        help='the path of the file with the words that should be ignored')
    parser.add_argument('counter', choices=['exact', 'bloom'],
                        help='the type of counter')

    args = vars(parser.parse_args())

    if args['counter'] == 'exact':
        counter = ExactCounter(args['text-file'].name, args['stopwords-file'].name)
    else:
        counter = BloomFilterCounter(args['text-file'].name, args['stopwords-file'].name)

    print(counter.count())
