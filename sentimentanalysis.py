'''
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/16/15
'''


'''

The basic signatures for our sentiment analysis. We will have to modify dictionary fill.
http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/ -- dictionary we will use. It contains
more information than we need, so we will try to reduce it to make our sentiment analysis easier.

'''

class SentimentAnalysis(object):

	'''
	Init Function
	'''

	def __init__(keyphrase_list, dictionary, desired_keyphrases):
		self.corrected_dictionary = _prune_dictionary(dictionary)
		self.keyphrase_value_list = _check_keyphrases(keyphrase_list, self.corrected_dictionary)
		self.selected_keyphrases = _choose_keyphrases(keyphrase_value_list, desired_keyphrases)


	'''
	Private Methods
	'''

	# Creates list of keyphrase values using the dictionary
	def _check_keyphrases(keyphrase_list, dictionary):
		return TODO

	# Choose the most powerful keyphrases based on sentiment
	def _choose_keyphrases(keyphrase_value_list, num_keyphrases):
		return TODO

	# Prune dictionary down to important words and their sentiments
	def _prune_dictionary(dictionary):
		return TODO

