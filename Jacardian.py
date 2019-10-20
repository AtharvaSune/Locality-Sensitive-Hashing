import pickle
from preprocess import preprocess


class Jaccardian():

	def __init__ (self, orginals_path, query_path):
		self.originals_path = orginals_path
		self.query_path = query_path
		self.processed_originals = process_originals(originals_path, train = true)

	def process_originals(path, train):
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


	def process_query(path, train):
		processed_query = {}

		op = preprocess(path, train, 'J')
	    processed_query = op.process()

    	return processed_query


	def compare(processed_originals, processed_query):


	def similarity():
		processed_query = process_query(self.query_path, train = true)

		# call compare for every query doc etc. and return accordingly

	

	
    