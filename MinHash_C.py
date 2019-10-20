import random
import math
from Shingle import Shingling


class MinHash():

    def __init__(self, shingle_dict, num_shingles, num_hashes):
        """
            MinHashing for implenting LSH
            @params:
                shingle_dict = dictionary pf shingles and their posting lists
                num_shingles = total number of shingles
                num_hashes   = total number of hash functions to be used
                               as default is 100 
        """
        self.num_hashes = num_hashes
        self.shingle_dict = shingle_dict
        self.shingle_id_dict = self.make_shingle_dict(shingle_dict)
        self.num_shingles = num_shingles

    def create_plane_matrix(self):
        plane = []
        for i in range(self.num_hashes):
            temp = []
            for j in range(self.num_shingles):
                rand = random.uniform(-1, 1)
                while rand in temp:
                    rand = random.uniform(-1, 1)
                temp.append(rand)
            plane.append(temp)

        return plane

    def make_shingle_dict(self, shingle_dict):
        """
            Maps the shingles to unique id's
            @params:
                shingle_dict

            @returns:
                a dictionary with keys as shingles and 
                values = unique number
        """
        temp = {}
        for i, key in enumerate(shingle_dict.keys()):
            temp[key] = i+1

        return temp

    def signature_matrix(self, dataset_size):
        # Initialize the signature matrix
        sm = []
        for i in range(self.num_hashes):
            temp = []
            for i in range(dataset_size):
                temp.append(0)
            sm.append(temp)

        sdm = []
        for i in range(self.num_shingles):
            t = []
            for j in range(dataset_size):
                t.append(0)
            sdm.append(t)

        for row in self.shingle_dict.keys():
            for col in self.shingle_dict[row]:
                sdm[self.shingle_id_dict[row]-1][col-1] = 1

        # Initialize the hash function coefficients
        plane = self.create_plane_matrix()
        for i in range(self.num_hashes):
            for j in range(dataset_size):
                t = 0
                for k in range(self.num_shingles):
                    t += sdm[k][j] * plane[i][k]
                sm[i][j] = t
        return sm


def main(path, train):
    shingles = Shingling(path)
    num_shingles, shingle_dict = shingles.k_shingles(
        shingles.create_dict_key(), train)
    print(num_shingles)
    dataset_size = shingles.print()
    min_H = MinHash(shingle_dict, num_shingles, dataset_size)
    f = open("/home/atharva/Desktop/Developement/LSH/sig_mat.txt", 'w')
    sig_m = min_H.signature_matrix(dataset_size)
    for i in sig_m:
        f.write(str(i))
        f.write("\n")
    f.close()


if __name__ == "__main__":
    main("/home/atharva/Desktop/Developement/LSH/corpus-20090418/org/*", True)
