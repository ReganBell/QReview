from collections import defaultdict
from nltk.corpus import stopwords
import math
import re

positivity_files = [('rt-polarity.neg', False), ('rt-polarity.pos', True)]
subjectivity_files = [('plot.tok.gt9.5000', False), ('quote.tok.gt9.5000', True)]

class Classifier:
    def __init__(self):
        self.load_dictionary(positivity_files, 0)
        self.load_dictionary(subjectivity_files, 1)

    def load_dictionary(self, files, switch):
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
        return self.evaluate(sentence, 0)

    def subjectivity(self, sentence):
        return self.evaluate(sentence, 1)

    def evaluate(self, sentence, switch):
        stop_words = stopwords.words('english')
        words = re.split("[ .?!]", sentence)
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
            if not (word in stop_words):
                if (len(word) > 2) & (word in vocabulary):
                    num_words += 1
                    prob_one += math.log(one_prob_dict.setdefault(word, 1.0/total_one_words))
                    prob_zero += math.log(zero_prob_dict.setdefault(word, 1.0/total_zero_words))
        prob_one = math.exp(prob_one)
        prob_zero = math.exp(prob_zero)
        return (prob_one - prob_zero) / (prob_one + prob_zero)

"""
    def subjectivity(self, sentence):
        stop_words = stopwords.words('english')
        words = sentence.split(" ")
        total_pos_words = self.pos_word_count + len(self.polar_vocab)
        total_neg_words = self.neg_word_count + len(self.polar_vocab)
        p = 0
        n = 0
        num_words = 0
        for word in words:
            word = word.lower()
            if not (word in stop_words):
                if word in self.polar_vocab:
                    num_words += 1
                    p += math.log(self.pos_prob_dict.setdefault(word, 1.0/total_pos_words))
                    n += math.log(self.neg_prob_dict.setdefault(word, 1.0/total_neg_words))
        p = math.exp(p)
        n = math.exp(n)
        return (p - n) / (p + n)
"""