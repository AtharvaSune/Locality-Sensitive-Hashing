from Shingle import Shingling
from MinHash import MinHash


def train(path, train):
    shingles = Shingling(path)
    shingle = shingles.k_shingles(shingles.create_dict_key())
    print(shingle)


if __name__ == "__main__":
    train("./corpus-20090418/test_d/g0pA_taska.txt*", False)
