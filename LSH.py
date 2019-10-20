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
            "a": [],
            "b": [],
            "c": 100 + 1
        }

        # generate coefficient a
        for i in range(0, 75):
            rand = random.randint(1, 100)
            while rand in coeff["a"]:
                rand = random.randint(1, 100)
            coeff["a"].append(rand)

        # generate coefficient b
        for i in range(0, 75):
            rand = random.randint(1, 100)
            while rand in coeff["b"]:
                rand = random.randint(1, 100)
            coeff["b"].append(rand)

        return coeff

    def process(self):
        for i in range(0, self.no_of_bands):
            for k in range(0, len(self.M[0][0])):
                v = []
                for j in range(0, self.band_size):
                    v.append(self.M[i][j][k])

                print(v)
        hash_functions = self.create_hash_functions()
        print(hash_functions)


if __name__ == "__main__":
    pass
