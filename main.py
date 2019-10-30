from Cosine import Cosine
from Jacardian import Jaccardian
from Hamming import Hamming
from Euclidean import Euclidean


def main(original_path, query_path):

    # define query doc here

    cosine = Cosine(original_path, query_path)
    jacardian = Jaccardian(original_path, query_path)
    hamming = Hamming(original_path, query_path)
    euclidean = Euclidean(original_path, query_path)
    print("Cosine similarity is:")
    print(cosine.similarity())

    print("Jacardian similarity is:")
    print(jacardian.similarity())

    print("Hamming similarity is:")
    print(hamming.similarity())

    print("Euclidean similarity is:")
    print(euclidean.similarity())


if __name__ == "__main__":
    main("/home/atharva/Desktop/Developement/LSH/corpus-20090418/org/*",
         "/home/atharva/Desktop/Developement/LSH/corpus-20090418/test_d/copy.txt*")
