import random
import math
import pickle


class MinHashC():

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

        flag = 1

        try:
            with open('min_hashc_functions', 'rb') as infile:
                plane = pickle.load(infile)
        except EnvironmentError:
            flag = 0

        if(flag == 1):
            return plane

        for i in range(self.num_hashes):
            temp = []
            for j in range(self.num_shingles):
                rand = random.uniform(-1, 1)
                while rand in temp:
                    rand = random.uniform(-1, 1)
                temp.append(rand)
            plane.append(temp)

        try:
            with open('min_hashc_functions', 'wb') as outfile:
                pickle.dump(plane, outfile)
        except EnvironmentError:
            flag = 0

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
