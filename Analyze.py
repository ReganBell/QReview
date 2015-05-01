"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/30/15
"""

import re
import math

from nltk.stem.snowball import EnglishStemmer
from nltk.corpus.reader.wordnet import Lemma
from nltk.corpus import wordnet

import Classifier
import HelperDicts

# helper methods for sentence similarity

def vector_operator(vector1, vector2, operator):
    """
    :type vector1: float list
    :type vector2: float list
    :type operator: function (float -> float -> float)
    :return: float list (vector): each element is operator applied to corresponding elements of given vectors
    """
    return [operator(vector1[i], vector2[i]) for i in range(0, len(vector1))]


def vector_sum(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float list (vector): vector sum of given vectors
    """
    return vector_operator(vector1, vector2, lambda a, b: a + b)


def vector_diff(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float list (vector): vector difference of given vectors
    """
    return vector_operator(vector1, vector2, lambda a, b: a - b)


def dot_product(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float: dot product of given vectors
    """
    to_return = 0
    for i in range(0, len(vector1)):
        to_return += vector1[i] * vector2[i]
    return to_return


def vector_length(vector):
    """
    :type vector: float list
    :return: float: length of given vector
    """
    return math.sqrt(dot_product(vector, vector))


def cosine_similarity(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float: between 0 and 1; cosine of angle between given vectors
    """
    return dot_product(vector1, vector2) / (vector_length(vector1) * vector_length(vector2))


def get_path_length_and_subsumer_height(word1, word2):
    """ see sections 2.3 and 2.4 of http://dx.doi.org.ezp-prod1.hul.harvard.edu/10.1109/TKDE.2003.1209005
    :type word1: string
    :type word2: string
    :return: (float, float): first is path length between given words, second is depth of subsumer along that path
    """
    concepts1 = wordnet.synsets(word1)
    concepts2 = wordnet.synsets(word2)
    shortest_path = None
    subsumers = None
    for concept1 in concepts1:
        for concept2 in concepts2:
            if concept1.pos() == concept2.pos():
                # case 1
                if concept1 == concept2:
                    return 0, 15
                # case 2
                words1 = map(Lemma.name, concept1.lemmas())
                words2 = map(Lemma.name, concept2.lemmas())
                for word1 in words1:
                    for word2 in words2:
                        if word1 == word2:
                            shortest_path = 1
                            subsumers = concept1.lowest_common_hypernyms(concept2)
                # case 3
                path_length = concept1.shortest_path_distance(concept2, simulate_root=True)
                if shortest_path is None or path_length < shortest_path:
                    shortest_path = path_length
                    subsumers = concept1.lowest_common_hypernyms(concept2)
    if shortest_path is None:
        shortest_path = 30
    if (subsumers is None) or (len(subsumers) == 0):
        subsumer_depth = 0
    else:
        subsumer_depth = subsumers[0].max_depth()
    return shortest_path, subsumer_depth


def similarity_score(word1, word2):
    """ see sections 2.3 and 2.4 of http://dx.doi.org.ezp-prod1.hul.harvard.edu/10.1109/TKDE.2003.1209005
    :type word1: string
    :type word2: string
    :return: float: between 0 and 1; similarity between two given words
    """
    stemmer = EnglishStemmer()
    if stemmer.stem(word1) == stemmer.stem(word2):
        return 1
    alpha = 0.2
    beta = 0.6
    l, h = get_path_length_and_subsumer_height(word1, word2)
    return math.exp((-1)*alpha*l)*((math.exp(beta*h)-math.exp((-1)*beta*h))/(math.exp(beta*h)+math.exp((-1)*beta*h)))


def semantic_vector_element(word, words, threshold):
    """ see section 2.1 of https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    :type word: string
    :type words: string list
    :param words: sentence representation (list of words)
    :type threshold: float
    :param threshold: between 0 and 1; the level at which two words are considered similar (1 = identical, 0 = perfectly dissimilar)
    :return: float: between 0 and 1; highest similarity between given word and sentence that meets threshold, else 0
    """
    if word in words:
        return 1
    else:
        highest_score = 0
        for other_word in words:
            score = similarity_score(word, other_word)
            if score > highest_score:
                highest_score = score
        return highest_score if highest_score > threshold else 0


def split_sentence(sentence):
    """
    :type sentence: string
    :return: string list: a list of each word in sentence, with punctuation removed and contractions expanded
    """
    words = map(lambda s: s.lower(), filter(None, re.split("[^a-zA-Z0-9'_]", sentence)))
    to_return = []
    for word in words:
        to_return += HelperDicts.expand_contractions(word).split(" ")
    return to_return


def semantic_similarity(sentence1, sentence2, threshold):
    """ see sections 2.1 of https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    :type sentence1: string
    :type sentence2: string
    :return: float: between 0 and 1; semantic similarity between two given sentences
    """
    words1, words2 = split_sentence(sentence1), split_sentence(sentence2)
    all_words = set(words1).union(set(words2))
    semantic_vector1, semantic_vector2 = [], []
    for word in all_words:
        semantic_vector1.append(semantic_vector_element(word, words1, threshold))
        semantic_vector2.append(semantic_vector_element(word, words2, threshold))
    return cosine_similarity(semantic_vector1, semantic_vector2)


def index_in(word, words, threshold):
    """
    :type word: string
    :type words: string list
    :param words: sentence representation (word list)
    :type threshold: float
    :param threshold: between 0 and 1; the level at which two words are considered similar (1 = identical, 0 = perfectly dissimilar)
    :return: int: index of word in given sentence most similar to given word (list of words); 0 if none found
    """
    highest_similarity = 0
    highest_index = None
    for index, other_word in enumerate(words):
        if other_word == word:
            return index+1
        else:
            similarity = similarity_score(word, other_word)
            if similarity > highest_similarity:
                highest_similarity = similarity
                highest_index = index+1
    return highest_index if highest_similarity > threshold else 0


def normalized_difference(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float: between
    """
    return 1.0 - (vector_length(vector_diff(vector1, vector2)) / vector_length(vector_sum(vector1, vector2)))


def word_order_similarity(sentence1, sentence2, threshold):
    """ see sections 2.3 of https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    :type sentence1: string
    :type sentence2: string
    :type threshold: float
    :param threshold: between 0 and 1; the level at which two words are considered similar (1 = identical, 0 = perfectly dissimilar)
    :return: float: between 0 and 1; word order similarity between two given sentences
    """
    words1, words2 = split_sentence(sentence1), split_sentence(sentence2)
    all_words = set(words1).union(set(words2))
    order_vector1, order_vector2 = [], []
    for word in all_words:
        order_vector1.append(index_in(word, words1, threshold))
        order_vector2.append(index_in(word, words2, threshold))
    return normalized_difference(order_vector1, order_vector2)


# sentence similarity

def sentence_similarity(sentence1, sentence2):
    """
    :type sentence1: string
    :type sentence2: string
    :return: float: between 0 and 1; similarity between given sentences (1 = identical; 0 = perfectly dissimilar)
    """
    semantic_threshold = 0.2
    order_threshold = 0.4
    semantic_weight = 0.85
    semantic = semantic_similarity(sentence1, sentence2, semantic_threshold)
    order = word_order_similarity(sentence1, sentence2, order_threshold)
    similarity = semantic_weight * semantic + (1 - semantic_weight) * order
    return similarity


def group_sentences_helper(sentence_groups):
    """
    :type sentence_groups: string list list
    :param sentence_groups: list of lists (groups) of sentences
    :return: a fully consolidated group of sentence groups (similar groups are combined)
    """
    threshold = 0.5
    max_similarity = 0
    first_index = None
    second_index = None
    for index1, sentence_group1 in enumerate(sentence_groups):
        for index2, sentence_group2 in enumerate(sentence_groups):
            if sentence_group1 != sentence_group2:
                min_local_similarity = 1
                for sentence1 in sentence_group1:
                    for sentence2 in sentence_group2:
                        similarity = sentence_similarity(sentence1, sentence2)
                        if similarity < min_local_similarity:
                            min_local_similarity = similarity
                if min_local_similarity > max_similarity:
                    max_similarity = min_local_similarity
                    first_index = index1
                    second_index = index2
    if max_similarity > threshold:
        new_sentence_groups = []
        for index, sentence_group in enumerate(sentence_groups):
            if (index != first_index) & (index != second_index):
                new_sentence_groups.append(sentence_group)
        new_sentence_groups.append(sentence_groups[first_index] + sentence_groups[second_index])
        return group_sentences_helper(new_sentence_groups)
    else:
        return sentence_groups


def group_sentences(sentences):
    return group_sentences_helper([[s] for s in sentences])


# sentiment analysis

class SentimentAnalysis:
    def __init__(self):
        """ initializes SentimentAnalysis object by loading the polarity lexicon into memory """
        f = open('sentiment-dictionary.tff', 'r')
        lines = f.readlines()
        f.close()
        dictionary = {}
        for line in lines:
            tokens = line.split()
            word = tokens[2].split('=')[1]
            polarity_string = tokens[5].split('=')[1]
            if polarity_string == "positive":
                polarity = 1.0
            elif polarity_string == "negative":
                polarity = -1.0
            else:
                polarity = 0.0
            subj = tokens[0].split('=')[1]
            if subj == 'strongsubj':
                strength = 2.0
            elif subj == 'weaksubj':
                strength = 1.0
            else:
                strength = 1.0
            dictionary[word] = polarity * strength
        self.dictionary = dictionary

    def positivity(self, sentence, keyword=""):
        """
        :type sentence: string
        :return: int: sign indicates positivity of given sentence, magnitude indicates strength (0 is neutral)
        """
        words = split_sentence(sentence)
        positivity = 0
        for index, word in enumerate(words):
            polarity = self.dictionary.get(word, None)
            if polarity is None:
                stemmer = EnglishStemmer()
                stemmed = stemmer.stem(word)
                polarity = self.dictionary.get(stemmed, 0)
            if polarity != 0:
                if word == keyword:
                    polarity *= 2.0
                if (index > 0):
                    polarity *= HelperDicts.modifier(words[index - 1])
                positivity += polarity
        return positivity


def analyze(keyword, phrases):
    """
    :type keyword: string
    :type phrases: string list
    :param phrases: list of phrases to analyze
    :return: tuple (string list, int) list: the string list are similar phrases, the int
             is 0, -1, and 1 for neutral, negative, and positive, respectively.
    """
    analyzer = SentimentAnalysis()
    groups = group_sentences(phrases)
    to_return = []
    for index, group in enumerate(groups):
        positivity = 0.0
        for phrase in group:
            positivity += analyzer.positivity(phrase, keyword)
        average_positivity = positivity / ((1.0) * len(group))
        if average_positivity >= 1:
            pos = 1
        elif average_positivity <= -1:
            pos = -1
        else:
            pos = 0
        to_return.append((group, pos))
    return to_return


def run():
    sentences = ["The big cat jumped over the moon","The big feline leaped above the lunar object", "The teacher likes to eat big apples",
                 "The big educator enjoys eating fruit","My brother climbs the big wall", "Big fat people eat cake"]
    print analyze("big", sentences)


#run()