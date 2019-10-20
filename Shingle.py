import glob
import os


class Shingling():
    def __init__(self, path, shingle_size=10):
        self.path = path[:-1]
        print(path)
        self.corpus = self.get_files(path)
        self.shingle_size = shingle_size
        self.train_data = {}

    def get_files(self, path):
        files = glob.glob(path)
        print(files)
        temp = []
        for file in files:
            temp.append(os.path.split(file)[1])
        print(temp)
        return temp

    def k_shingles(self, corpus_key, train=True):
        a = set()
        for file in self.corpus:
            path = self.path + file
            f = open(path, 'r', encoding="unicode_escape").read().strip()
            f = f.replace("\n", " ")
            f = f.replace(",", "")
            f = f.replace(".", "")
            for i in range(len(f)-self.shingle_size):
                key = f[i:i+self.shingle_size]
                a.add(key)
                if train:
                    if key in self.train_data.keys():
                        self.train_data[key].append(corpus_key[file])
                        self.train_data[key] = list(set(self.train_data[key]))
                    else:
                        self.train_data[key] = []
                        self.train_data[key].append(corpus_key[file])
        if train:
            return len(list(a)), self.train_data
        else:
            return list(a)

    def create_dict_key(self):
        corpus_key = {}

        for i, file in enumerate(self.corpus):
            corpus_key[file] = i+1

        return corpus_key

    def print(self):
        f = open("/home/atharva/Desktop/Developement/LSH/out.txt",
                 'w')
        for key in self.train_data.keys():
            f.write("{}:{}\n".format(key, self.train_data[key]))
        f.close()
        print("Shingle Dictionary Created")
        return len(self.corpus)


if __name__ == "__main__":
    pre = Shingling("./corpus-20090418/*")
    pre.k_shingles(pre.create_dict_key())
    pre.print()
