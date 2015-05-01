"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/30/15
"""

from collections import defaultdict
from nltk.corpus import stopwords
from math import log, exp
from re import split

positivity_files = [('rt-polarity.neg', False), ('rt-polarity.pos', True)]
subjectivity_files = [('plot.tok.gt9.5000', False), ('quote.tok.gt9.5000', True)]


class Classifier:
    def __init__(self):
        """ trains the classifier on the positivity and subjectivity corpora """
        self.train(positivity_files, 0)
        self.train(subjectivity_files, 1)

    def train(self, files, switch):
        """
        :type files: (string, boolean) list
        :param files: list of size 2; the string is the filename to learn on, the boolean
                refers to which data is being trained (False for negative, True for positive)
        :type switch: int
        :param switch: 0 or 1: 0 to train positivity, 1 to train subjectivity
        :return: None (dictionary is loaded as instance variable)
        """
        vocabulary = set()
        one_count_dict = defaultdict(float)
        zero_count_dict = defaultdict(float)
        one_word_count = 0
        zero_word_count = 0
        for file in files:
            filename, one = file
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                words = line.split(" ")
                for word in words:
                    if len(word) > 2:
                        vocabulary.add(word)
                        if one:
                            one_word_count += 1
                            one_count_dict[word] += 1
                        else:
                            zero_word_count += 1
                            zero_count_dict[word] += 1
        one_prob_dict = dict()
        zero_prob_dict = dict()
        for positive in [False, True]:
            for word in vocabulary:
                if positive:
                    one_prob_dict[word] = (one_count_dict[word]+1.0)/(one_word_count+len(vocabulary))
                else:
                    zero_prob_dict[word] = (zero_count_dict[word]+1.0)/(zero_word_count+len(vocabulary))
        if switch == 0:
            self.polar_vocab = vocabulary
            self.pos_word_count = one_word_count
            self.pos_prob_dict = one_prob_dict
            self.neg_word_count = zero_word_count
            self.neg_prob_dict = zero_prob_dict
        else:
            self.objective_vocab = vocabulary
            self.obj_word_count = one_word_count
            self.obj_prob_dict = one_prob_dict
            self.subj_word_count = zero_word_count
            self.subj_prob_dict = zero_prob_dict

    def positivity(self, sentence):
        """
        :type sentence: string
        :param sentence: long sentences (above a dozen words) decrease accuracy
        :return: float: between -1 and 1; positivity of given sentence (-1 for completely negative, 1 for completely positive. 0 is ambiguous
        """
        return self.evaluate(sentence, 0)

    def subjectivity(self, sentence):
        """
        :type sentence: string
        :param sentence: long sentences (above a dozen words) decrease accuracy
        :return: float: between -1 and 1; subjectivity of given sentence (-1 for completely objective, 1 for completely subjective. 0 is ambiguous
        """
        return self.evaluate(sentence, 1)

    def evaluate(self, sentence, switch):
        """
        :type sentence: string
        :param sentence: long sentences (above a dozen words) decrease accuracy
        :type switch: int
        :param switch: 0 or 1: 0 to evaluate positivity of given sentence, 1 to evaluate subjectivity of given sentence
        :return: float: between -1 and 1; positivity/subjectivity of given sentence (-1 for the opposite, 1 for the most)
        """
        stop_words = stopwords.words('english')
        words = filter(None, split("[^a-zA-Z0-9'_]", sentence))
        if switch == 0:
            vocabulary = self.polar_vocab
            one_word_count = self.pos_word_count
            zero_word_count = self.neg_word_count
            one_prob_dict = self.pos_prob_dict
            zero_prob_dict = self.neg_prob_dict
        else:
            vocabulary = self.objective_vocab
            one_word_count = self.obj_word_count
            zero_word_count = self.subj_word_count
            one_prob_dict = self.obj_prob_dict
            zero_prob_dict = self.subj_prob_dict
        total_one_words = one_word_count + len(vocabulary)
        total_zero_words = zero_word_count + len(vocabulary)
        prob_one = 0
        prob_zero = 0
        num_words = 0
        for word in words:
            word = word.lower()
            if word not in stop_words:
                if (len(word) > 2) & (word in vocabulary):
                    num_words += 1
                    prob_one += log(one_prob_dict.get(word, 1.0/total_one_words))
                    prob_zero += log(zero_prob_dict.get(word, 1.0/total_zero_words))
        prob_one = exp(prob_one)
        prob_zero = exp(prob_zero)
        return (prob_one - prob_zero) / (prob_one + prob_zero)