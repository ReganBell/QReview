"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/16/15
"""

import re
import math


# helper methods for sentence similarity


def dot_product(vector1, vector2):
    """
    :param vector1: list of floats (vector)
    :param vector2: list of floats (assumed same length as l1, vector)
    :return: dot product of given vectors (sum of products of corresponding elements)
    """
    to_return = 0
    for i in range(0, len(vector1)):
        to_return += vector1[i] * vector2[i]
    return to_return


def vector_length(vector):
    """
    :param vector: list of integers (vector)
    :return: float, length of given vector
    """
    return math.sqrt(dot_product(vector, vector))


def cosine_similarity(vector1, vector2):
    """
    :param vector1: list of floats (vector)
    :param vector2: list of floats (assumed same length as l1, vector)
    :return: float, cosine of angle between given vectors (from 0 if vectors are anti-parallel to 1 if they're parallel)
    """
    return dot_product(vector1, vector2) / (vector_length(vector1) * vector_length(vector2))


def similarity_score(word1, word2):
    """
    :param word1: string (word)
    :param word2: string (word)
    :return: string as section 2.2 of https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    """
    return 0


def semantic_vector_element(word, words, threshold):
    """
    :param word: string (word)
    :param words: list of strings (words)
    :param threshold: float (between 0 and 1, minimum nonzero level of similarity permitted)
    :return: float, the maximum semantic similarity between given word and a word int the given list, if above threshold
    """
    if word in words:
        return 1
    else:
        highest_score = 0
        for word1 in words:
            score = similarity_score(word, word1)
            if score > highest_score:
                highest_score = score
        if highest_score > threshold:
            return highest_score
        else:
            return 0


def semantic_similarity(sentence1, sentence2, threshold):
    """
    :param sentence1: string (sentence)
    :param sentence2: string (sentence)
    :param threshold: float (between 0 and 1, minimum nonzero level of similarity permitted)
    :return: string, as section 2.1 of https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    """
    words1 = set(re.split("[\W]", sentence1))
    words2 = set(re.split("[\W]", sentence2))
    all_words = words1.union(words2)
    semantic_vector1 = []
    semantic_vector2 = []
    for word in all_words:
        semantic_vector1.append(semantic_vector_element(word, words1, threshold))
        semantic_vector2.append(semantic_vector_element(word, words2, threshold))
    return cosine_similarity(semantic_vector1, semantic_vector2)


# sentence similarity


def sentence_similarity(s1, s2):
    """
    :param s1: first sentence (string)
    :param s2: second sentence (string)
    :return: string, sentence similarity as defined by https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    """
    semantic_similarity_threshold = 0.2
    word_order_threshold = 0.4
    semantic_similarity_weight = 0.85

    semantic = semantic_similarity(s1, s2, semantic_similarity_threshold)
    order = 0
    similarity = semantic_similarity_weight * semantic + (1 - semantic_similarity_weight) * order
    return similarity


# sentiment analysis


def get_dictionary():
    f = open('sentiment-dictionary.tff', 'r')
    list = f.readlines()
    f.close()
    dict = {}
    for line in list:
        tokens = line.split()
        word = tokens[2].split('=')[1]
        polarity_string = tokens[5].split('=')[1]
        if polarity_string == "positive":
            polarity = 1
        elif polarity_string == "negative":
            polarity = -1
        else:
            polarity = 0
        subj = tokens[0].split('=')[1]
        if subj == 'strongsubj':
            strength = 2
        elif subj == 'weaksubj':
            strength = 1
        else:
            strength = 1
        dict[word] = polarity * strength
    return dict


def sentiment(sentence, dictionary):
    tokens = re.split("[\W]",sentence)
    polarity = 0
    for word in tokens:
        polarity += dictionary.get(word, 0)
    return polarity
