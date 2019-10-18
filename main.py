import argparse
from shingle import Shingling


def main(path, train=True):
    shingles = Shingling()
    shingles.k_shingles(shingles.create_dict_key(), train)
    shingles.print()


if __name__ == "__main__":
    main()
