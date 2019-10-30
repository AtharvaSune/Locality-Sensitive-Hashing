import random
import math
from Shingle import Shingling
import pickle


class MinHashE():

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

    def create_euclidean_matrix(self, width):
        euclid, b = [], []
        flag = 1

        try:
            with open('min_hashe_functions', 'rb') as infile:
                euclid = pickle.load(infile)
        except EnvironmentError:
            flag = 0
        try:
            with open('min_hasheb_functions', 'rb') as infile:
                b = pickle.load(infile)
        except EnvironmentError:
            flag = 0
        if flag == 1:
            return euclid, b

        for i in range(self.num_hashes):
            temp = []
            for j in range(self.num_shingles):
                rand = random.gauss(0, 1)
                while rand in temp:
                    rand = random.gauss(0, 1)
                temp.append(rand)
            euclid.append(temp)
        for i in range(self.num_hashes):
            rand = random.uniform(0, width)
            while rand in temp:
                rand = random.uniform(0, width)
            b.append(rand)

        try:
            with open('min_hashe_functions', 'wb') as outfile:
                pickle.dump(euclid, outfile)
        except EnvironmentError:
            flag = 0

        try:
            with open('min_hasheb_functions', 'wb') as outfile:
                pickle.dump(b, outfile)
        except EnvironmentError:
            flag = 0

        return euclid, b

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

    def signature_matrix(self, dataset_size, width, shingles_list=[], train=True):
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

        if train:
            for row in self.shingle_dict.keys():
                for col in self.shingle_dict[row]:
                    sdm[self.shingle_id_dict[row]-1][col-1] = 1
        else:
            for row in self.shingle_dict.keys():
                if row in shingles_list:
                    sdm[self.shingle_id_dict[row]-1][0] = 1

        # Initialize the hash function coefficients
        euclid, b = self.create_euclidean_matrix(width)

        for i in range(self.num_hashes):
            for j in range(dataset_size):
                t = 0
                for k in range(self.num_shingles):
                    t += sdm[k][j] * euclid[i][k]
                sm[i][j] = (t + b[i]) // width
                if sm[i][j] < 0:
                    sm[i][j] = abs(sm[i][j])
                sm[i][j] = int(sm[i][j])
        return sm


if __name__ == "__main__":
    pass
    # main("/home/atharva/Desktop/Developement/LSH/corpus-20090418/org/*", True)
