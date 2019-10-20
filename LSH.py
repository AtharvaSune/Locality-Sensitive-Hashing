import random


class LSH:
    def __init__(self, signature_matrix, no_of_bands):
        self.M = []
        self.no_of_bands = no_of_bands
        self.signature_matrix = signature_matrix
        self.band_size = len(signature_matrix) // no_of_bands
        self.make_bands()
        self.process()

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

        return coeff

    # return candidate pairs for given band, calculated for 100 hash funcitons
    def band_candidates(self, band_condensed):
        docs = len(band_condensed)

        candidate_pairs = [[0] * docs] * docs

        for i in range(0, 100):
            a = coeff['a'][i]
            b = coeff['b'][i]
            c = coeff['c']

            hashed_docs = {}

            for j in range(0, len(band_condensed)):
                val = (a * band_condensed[j] + b) % c
                if(val not in hashed_docs):
                    hashed_docs[val] = list()
                hashed_docs[val].append(j)

            for k in hashed_docs:
                for doc in range(0, len(hashed_docs[k] - 1)):
                    for doc2 in range(doc + 1, len(hashed_docs[k])):
                        candidate_pairs[doc][doc2] += 1
                        candidate_pairs[doc2][doc] += 1

        res = dict()

        for i in range(0, docs):
            res[i] = list()

            for j in range(0, docs):
                if(i != j and candidate_pairs[i][j] >= 60):
                    res[i].append(j)

        return res

    def process(self):
        for i in range(0, self.no_of_bands):
            for k in range(0, len(self.M[0][0])):
                band_condensed = []
                v = []
                for j in range(0, self.band_size):
                    v.append(self.M[i][j][k])

                band_condensed.append(int("".join(map(str, v))))

                print(v)
        hash_functions = self.create_hash_functions()
        print(hash_functions)


if __name__ == "__main__":
    pass
