import random
import pickle
from Shingle import Shingling
from MinHash_C import MinHashC
from MinHash_J import MinHashJ
from MinHash_H import MinHashH
from Shingle import Shingling
from MinHash_E import MinHashE


class preprocess:
    def __init__(self, path, train, sm_type):
        self.M = []
        self.no_of_bands = 20
        self.signature_matrix = self.create_sm(path, train, sm_type)
        self.band_size = len(self.signature_matrix) // self.no_of_bands
        self.make_bands()
        # self.process()

    def create_sm(self, path, train, sm_type):
        shingles = Shingling(path)
        if train:
            num_shingles, shingle_dict = shingles.k_shingles(
                shingles.create_dict_key(), train)
            try:
                with open('shingle_dictionary', 'wb') as outfile:
                    pickle.dump(shingle_dict, outfile)
            except EnvironmentError:
                pass
        else:
            try:
                with open('shingle_dictionary', 'rb') as infile:
                    shingle_dict = pickle.load(infile)
                    num_shingles = len(shingle_dict.keys())
            except EnvironmentError:
                pass
            shingle_list = shingles.k_shingles(
                shingles.create_dict_key(), train)

        dataset_size = shingles.print()
        if(sm_type == 'J'):
            min_H = MinHashJ(shingle_dict, num_shingles, 100)
        elif(sm_type == 'C'):
            min_H = MinHashC(shingle_dict, num_shingles, 100)
        elif(sm_type == "E"):
            min_H = MinHashE(shingle_dict, num_shingles, 100)
        else:
            min_H = MinHashH(shingle_dict, num_shingles, 100)

        if train:
            if sm_type != "E":
                sig_m = min_H.signature_matrix(dataset_size)
            else:
                sig_m = min_H.signature_matrix(dataset_size, self.no_of_bands)
        else:
            if sm_type != "E":
                sig_m = min_H.signature_matrix(
                    dataset_size, shingle_list, False)
            else:
                sig_m = min_H.signature_matrix(
                    dataset_size, self.no_of_bands, shingle_list, False)

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

    def create_hash_functions(self):
        """
            Hash functions will be of the form h(x) = (a*x + b) mod c
            where   a = number less than max value of x
                    b = number less than max value of x
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
        for i in range(0, 100):
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
    def calc_hashes(self, condensed_list):

        processed_doc = {}
        coeff = self.create_hash_functions()
        for i in range(0, len(condensed_list)):
            processed_doc[i+1] = list()

            for j in range(0, 100):
                a = coeff['a'][j]
                b = coeff['b'][j]
                c = coeff['c']

                val = (a * condensed_list[i] + b) % c
                processed_doc[i+1].append(val)

        return processed_doc

    def process(self):
        processed_originals = {}

        for i in range(0, len(self.M[0][0])):  # column size # in every column
            condensed_list = list()

            for j in range(0, self.no_of_bands):  # for every band of column
                v = []
                for k in range(0, self.band_size):  # for every row of band
                    v.append(self.M[j][k][i])

                band_condensed = (int("".join(map(str, v))))
                condensed_list.append(band_condensed)
            processed_originals[i] = self.calc_hashes(condensed_list)
        return processed_originals
