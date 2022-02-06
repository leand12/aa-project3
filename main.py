import argparse
from counter import ExactCounter, BloomFilterCounter


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Distinct Word Counting Program')

    parser.add_argument('file', type=argparse.FileType('r'),
                        help='the path of the file with the words to be counted')
    parser.add_argument('counter', choices=['exact', 'bloom'],
                        help='the type of counter')

    args = parser.parse_args()

    exact = ExactCounter(args.file.name)
    bloom = BloomFilterCounter(args.file.name)

    exact.read_chars()
