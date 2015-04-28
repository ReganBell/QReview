"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/16/15
"""

import re
import math
import nltk
from nltk.corpus import wordnet as wn


# helper methods for sentence similarity

def vector_operator(vector1, vector2, operator):
    to_return = []
    for i in range(0, len(vector1)):
        to_return.append(operator(vector1[i], vector2[i]))
    return to_return

def vector_sum(vector1, vector2):
    return vector_operator(vector1, vector2, lambda a, b: a + b)

def vector_diff(vector1, vector2):
    return vector_operator(vector1, vector2, lambda a, b: a - b)

def dot_product(vector1, vector2):
    to_return = 0
    for i in range(0, len(vector1)):
        to_return += vector1[i] * vector2[i]
    return to_return

def vector_length(vector):
    return math.sqrt(dot_product(vector, vector))

def cosine_similarity(vector1, vector2):
    return dot_product(vector1, vector2) / (vector_length(vector1) * vector_length(vector2))

def case_1(word1, word2):
    concepts1 = wn.synsets(word1)
    concepts2 = wn.synsets(word2)
    for concept1 in concepts1:
        for concept2 in concepts2:
            if concept1 == concept2:
                return True
    return False

def case_2(word1, word2):
    concepts1 = wn.synsets(word1)
    concepts2 = wn.synsets(word2)
    for concept1 in concepts1:
        for concept2 in concepts2:
            words1 = map(nltk.corpus.reader.wordnet.Lemma.name, concept1.lemmas())
            words2 = map(nltk.corpus.reader.wordnet.Lemma.name, concept2.lemmas())
            for word1 in words1:
                for word2 in words2:
                    if word1 == word2:
                        return True
    return False

def get_path_length(word1, word2):
    if case_1(word1, word2):
        return 0
    elif case_2(word1, word2):
        return 1
    else:
        concepts1 = wn.synsets(word1)
        concepts2 = wn.synsets(word2)
        shortest_path = None
        for concept1 in concepts1:
            for concept2 in concepts2:
                if concept1.pos() == concept2.pos():
                    path_length = concept1.shortest_path_distance(concept2, simulate_root=True)
                    if shortest_path is None:
                        shortest_path = path_length
                    elif path_length < shortest_path:
                        shortest_path = path_length
        if shortest_path is None:
            return 0
        else:
            return shortest_path

def get_subsumer_height(word1, word2):
    concepts1 = wn.synsets(word1)
    concepts2 = wn.synsets(word2)
    shortest_path = None
    subsumers = None
    for concept1 in concepts1:
        for concept2 in concepts2:
            if concept1.pos() == concept2.pos():
                path_length = concept1.shortest_path_distance(concept2, simulate_root=True)
                if shortest_path is None:
                    shortest_path = path_length
                    subsumers = concept1.lowest_common_hypernyms(concept2)
                elif path_length < shortest_path:
                    shortest_path = path_length
                    subsumers = concept1.lowest_common_hypernyms(concept2)
    if (subsumers is None) or (len(subsumers) == 0):
        return 0
    else:
        return subsumers[0].max_depth()

def similarity_score(word1, word2):
    alpha = 0.2
    beta = 0.6
    l = get_path_length(word1, word2)
    h = get_subsumer_height(word1, word2)
    return math.exp((-1)*alpha*l)*((math.exp(beta*h)-math.exp((-1)*beta*h))/(math.exp(beta*h)+math.exp((-1)*beta*h)))

def semantic_vector_element(word, words, threshold):
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
    words1 = re.split("[\W]", sentence1)
    words2 = re.split("[\W]", sentence2)
    all_words = set(words1).union(set(words2))
    semantic_vector1 = []
    semantic_vector2 = []
    for word in all_words:
        semantic_vector1.append(semantic_vector_element(word, words1, threshold))
        semantic_vector2.append(semantic_vector_element(word, words2, threshold))
    return cosine_similarity(semantic_vector1, semantic_vector2)

def index_in(word, words, threshold):
    highest_similarity = 0
    highest_index = None
    for index, word1 in enumerate(words):
        if word1 == word:
            return index
        else:
            similarity = similarity_score(word, word1)
            if similarity > highest_similarity:
                highest_similarity = similarity
                highest_index = index
    if highest_similarity > threshold:
        return highest_index
    else:
        return 0

def normalized_difference(vector1, vector2):
    return 1 - (vector_length(vector_diff(vector1, vector2)) / vector_length(vector_sum(vector1, vector2)))

def word_order_similarity(sentence1, sentence2, threshold):
    words1 = re.split("[\W]", sentence1)
    words2 = re.split("[\W]", sentence2)
    all_words = set(words1).union(set(words2))
    order_vector1 = []
    order_vector2 = []
    for word in all_words:
        order_vector1.append(index_in(word, words1, threshold))
        order_vector2.append(index_in(word, words2, threshold))
    return normalized_difference(order_vector1, order_vector2)


# sentence similarity

def sentence_similarity(sentence1, sentence2):
    similarity_threshold = 0.2
    order_threshold = 0.4
    semantic_weight = 0.85
    semantic = semantic_similarity(sentence1, sentence2, similarity_threshold)
    order = word_order_similarity(sentence1, sentence2, order_threshold)
    similarity = semantic_weight * semantic + (1 - semantic_weight) * order
    return similarity


# sentiment analysis

def get_dictionary():
    f = open('sentiment-dictionary.tff', 'r')
    lines = f.readlines()
    f.close()
    dictionary = {}
    for line in lines:
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
        dictionary[word] = polarity * strength
    return dictionary


def sentiment(sentence, dictionary):
    tokens = re.split("[\W]",sentence)
    polarity = 0
    for word in tokens:
        polarity += dictionary.get(word, 0)
    return polarity