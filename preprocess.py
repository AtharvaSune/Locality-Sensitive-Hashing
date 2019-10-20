import random
import pickle
from Shingle import Shingling
from MinHash_C import MinHashC
from MinHash_J import MinHashJ
from MinHash_H import MinHashH

class preprocess:
    def __init__(self, path, train, sm_type):
        self.M = []
        self.no_of_bands = 20
        self.signature_matrix = create_sm(path, train, sm_type)
        self.band_size = len(signature_matrix) // no_of_bands
        self.make_bands()
        self.process()

    def create_sm(path, train, sm_type):
        shingles = Shingling(path)
        num_shingles, shingle_dict = shingles.k_shingles(
            shingles.create_dict_key(), train)
        dataset_size = shingles.print()

        if(sm_type == 'J'):
            min_H = MinHashJ(shingle_dict, num_shingles, dataset_size)
        else if(sm_type == 'C'):
            min_H = MinHashc(shingle_dict, num_shingles, dataset_size)
        else:
            min_H = MinHashH(shingle_dict, num_shingles, dataset_size)

        sig_m = min_H.signature_matrix(dataset_size)

        return sig_m


    def make_bands(self):
        """
            Makes 'b' bands of size 'k' each from the input signature matrix
        """
        for j in range(0, self.no_of_bands):
            k = []
            for i in range(0, self.band_size):
                k.append(self.signature_matrix[j * self.band_size + i])
            self.M.append(k)
        # print(self.M)

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
            with open('lsh_hash_functions', 'rb') as infile:
                persistant_coeff = pickle.load(infile)

        except EnvironmentError:
            flag = 0

        if(flag == 1):
            return persistant_coeff

        coeff = {
            'a': [],
            'b': [],
            'c': 100 + 1
        }

        # generate coefficient a
        for i in range(0, 75100):
            rand = random.randint(1, 100)
            while rand in coeff['a']:
                rand = random.randint(1, 100)
            coeff['a'].append(rand)

        # generate coefficient b
        for i in range(0, 100):
            rand = random.randint(1, 100)
            while rand in coeff['b']:
                rand = random.randint(1, 100)
            coeff['b'].append(rand)

        try:
            with open('lsh_hash_functions', 'wb') as outfile:
                pickle.dump(coeff, outfile)

        except EnvironmentError:
            flag = 0

        return coeff

    # return candidate pairs for given band, calculated for 100 hash funcitons
    def calc_hashes(condensed_list):

        processed_doc = {}

        for i in range(0, len(condensed_list)):
            processed_doc[i] = list()

            for i in range(0, 100):
                a = coeff['a'][i]
                b = coeff['b'][i]
                c = coeff['c']

                val = (a * band_condensed[j] + b) % c
                processed_doc[i].append(val)

        return processed_doc

    def process(self):

        processed_originals = {}

        for i in range(0, len(self.M[0][0])): #column size # in every column
            condensed_list = list()

            for j in range(0, self.no_of_bands): #for every band of column
                v = []
                for k in range(0, self.band_size): #for every row of band
                    v.append(self.M[j][k][i])

                band_condensed = (int("".join(map(str, v))))
                condensed_list.append(band_condensed)

            processed_originals[i] = calc_hashes(condensed_list)


        return processed_originals
