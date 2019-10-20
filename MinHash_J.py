import random
import math
import pickle
from shingle import Shingling


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

    def create_hash_functions(self):
        """
            Hash functions will be of the form h(x) = (a*x + b) mod c
            where   a = number less tha max value of x
                    b = number less tha max value of x
                    c = max value of x + 1

            This function will return a dictionary where key = coeff a, b 
            and the value is a list of size num_hashes
        """
        flag = 1

        persistant_coeff = {}

        try:
            with open('min_hashj_functions', 'rb') as infile:
                persistant_coeff = pickle.load(infile)

        except EnvironmentError:
            flag = 0

        if(flag == 1):
            return persistant_coeff

        coeff = {
            'a': [],
            'b': [],
            'c': self.num_shingles + 1
        }

        # generate coefficient a
        for i in range(0, self.num_hashes):
            rand = random.randint(1, self.num_shingles)
            while rand in coeff['a']:
                rand = random.randint(1, self.num_shingles)
            coeff['a'].append(rand)

        # generate coefficient b
        for i in range(0, self.num_hashes):
            rand = random.randint(1, self.num_shingles)
            while rand in coeff['b']:
                rand = random.randint(1, self.num_shingles)
            coeff['b'].append(rand)

        try:
            with open('min_hash_functions', 'wb') as outfile:
                pickle.dump(coeff, outfile)

        except EnvironmentError:
            flag = 0

        return coeff

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
                temp.append(math.inf)
            sm.append(temp)
        # Initialize the hash function coefficients
        coeff = self.create_hash_functions()
        # implement min_hashing following the psuedo code
        # in psuedo.md
        for row in self.shingle_dict.keys():
            hash_value = []

            for i in range(self.num_hashes):
                # calculate hash values for considered row
                # where hash functions are of format
                # h(x) = (a*x + b) % c
                val = (coeff['a'][i] * self.shingle_id_dict[row] +
                       coeff['b'][i]) % coeff['c']
                hash_value.append(val)

            # M(i, c) = min(M(i, c), val(i)) for given row
            # c = column that contains the considered shingle
            # i = ith hash function
            for c in self.shingle_dict[row]:
                for i, hash_val in enumerate(hash_value):
                    sm[i][c-1] = min(sm[i][c-1], hash_val)
        return sm
