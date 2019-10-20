import random
import math
from Shingle import Shingling

random.seed(1)

class MinHashH():

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
        sm, temp = [], []
        for i in range(self.num_shingles):
            temp.append(i+1)
        random.shuffle(temp)
        temp = temp[:self.num_hashes+1]
        print("temp: {}".format(temp))
        sdm = []
        for i in range(self.num_shingles):
            t = []
            for j in range(dataset_size):
                t.append(0)
            sdm.append(t)

        for row in self.shingle_dict.keys():
            for col in self.shingle_dict[row]:
                sdm[self.shingle_id_dict[row]-1][col-1] = 1

        for i in range(self.num_hashes):
            sm.append(sdm[temp[i]])
        return sm
