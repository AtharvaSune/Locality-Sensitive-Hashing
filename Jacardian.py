import pickle
from preprocess import preprocess


class Jaccardian():

    def __init__(self, originals_path, query_path):
        self.originals_path = originals_path
        self.query_path = query_path
        self.processed_originals = self.process_originals(
            originals_path, train=True)
        self.processed_query = {}

    def process_originals(self, path, train):
        processed_originals = {}

        flag = 1

        try:
            with open('processed_originals_jac', 'rb') as infile:
                processed_originals = pickle.load(infile)
        except EnvironmentError:
            flag = 0

        if(flag == 1):
            return processed_originals

        op = preprocess(path, train, 'J')
        processed_originals = op.process()

        with open('processed_originals_jac', 'wb') as outfile:
            pickle.dump(processed_originals, outfile)

        return processed_originals

    def process_query(self, path, train):
        processed_query = {}

        op = preprocess(path, train, 'J')
        processed_query = op.process()

        return processed_query

    def compare(self, original, query):
        org_column = self.processed_originals[original]
        query_column = self.processed_query[query]

        similar_bands = 0

        for band in org_column:
            hash_count = 0

            for hash_ind in range(0, len(org_column[band])):
                if(org_column[band][hash_ind] == query_column[band][hash_ind]):
                    hash_count += 1

            if(hash_count >= 60):
                similar_bands += 1

        similar = similar_bands / 20
        comparison = False

        if (similar >= 0.6):
            comparison = True

        return comparison, similar

    def similarity(self):
        self.processed_query = self.process_query(self.query_path, train=False)
        res = dict()

        for original in self.processed_originals:
            res[original] = dict()
            comparison, similar = self.compare(original, 0)
            res[original]['comparison'] = comparison
            res[original]['similar'] = similar

        return res
        # call compare for every query doc etc. and return accordingly
