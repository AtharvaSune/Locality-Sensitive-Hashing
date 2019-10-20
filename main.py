from Cosine import Cosine
from Jacardian import jacardian
from Hamming import Hamming

def main():

	 #define query doc here

	 cosine = Cosine(original_path, query_path)
	 jacardian = Jacardian(original_path, query_path)
	 hamming = Hamming(original_path, query_path)

	 print("Cosine similarity is:")
	 print(cosine.similarity())

	 print("Jacardian similarity is:")
	 print(jacardian.similarity())

	 print("Hamming similarity is:")
	 print(hamming.similarity())

