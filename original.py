import argparse
from MinHash import main


def main1(path, train=True):
    main(path, train)


if __name__ == "__main__":
    main1("/home/atharva/Desktop/Developement/LSH/corpus-20090418/org/*")
