"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/30/15
"""

import re

from nltk.stem.snowball import EnglishStemmer
from nltk.corpus.reader.wordnet import Lemma
from nltk.corpus import wordnet

import math
import Classifier
import Contractions


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
                    return 0, concept1.max_depth()
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
        to_return += Contractions.expand_contractions(word).split(" ")
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


def similarity_matrix(sentences):
    matrix = [[]]
    for row, sentence1 in enumerate(sentences):
        for col, sentence2 in enumerate(sentences):
            if sentence1 == sentence2:
                matrix[row][col] = 0
            else:
                matrix[row][col] = sentence_similarity(sentence1, sentence2)
    print matrix



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
        self.dictionary = dictionary

    def positivity(self, sentence, keyword=""):
        """
        :type sentence: string
        :return: int: sign indicates positivity of given sentence, magnitude indicates strength (0 is neutral)
        """
        words = split_sentence(sentence)
        positivity = 0
        stemmer = EnglishStemmer()
        for index, word in enumerate(words):
            stemmed = stemmer.stem(word)
            polarity = self.dictionary.get(stemmed, 0)
            if word == keyword:
                polarity *= 2
            if (index > 0) & (words[index - 1] == "not"):
                positivity -= polarity
            else:
                positivity += polarity
        return positivity


def extract_similar(phrases):
    similar_group = [[s] for s in phrases]
    for phrase in phrases[1:]:
        for group in similar_group:
            similar = True
            for sentence1 in group:
                similarity = sentence_similarity(phrase, sentence1)
                if similarity < 0.6 or phrase == sentence1:
                    similar = False
                    break
            if similar:
                group.append(phrase)
    return similar_group

def run():
    sentence1 = "They're my best friends"
    sentence2 = "Those people are my closest companions"

    print "sentence similarity: {0:.3f}".format(sentence_similarity(sentence1, sentence2))

    classifier = Classifier.Classifier()
    analyzer = SentimentAnalysis()
    print 'subjectivity: {0:.2f}'.format(classifier.subjectivity(sentence1))
    print 'analyzer positivity: {}'.format(analyzer.positivity(sentence1))
    print 'classifier positivity: {0:.2f}'.format(classifier.positivity(sentence1))

    """
    courses = TextRank.parse_course_file("2014QComments")
    for index, course in enumerate(courses[0:1]):
        # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
        parts_of_speech = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
        window = 2
        custom_stop_words = ["course", "class"]
        min_keyword_length = 2
        key_phrases = TextRank.key_phrases_for_course(course, parts_of_speech, window, custom_stop_words, min_keyword_length)
        print index+1, course[0]
        for key_phrase in key_phrases:
            print key_phrase
            sentences = []
            phrases = []
            sentences = []
            for comment in course[1]:
                for sentence in re.split("[.?!]", comment):
                    key_phrase_indices = []
                    words = re.split("[\W]",sentence)
                    for index, word in enumerate(words):
                        if word == key_phrase:
                            sentences.append(sentence)
                            key_phrase_indices.append(index)
                    for index in key_phrase_indices:
                        lower_index = index - 5
                        upper_index = index + 5
                        if lower_index < 0:
                            lower_index = 0
                        if upper_index > len(words):
                            upper_index = len(words)
                        phrase = ' '.join(words[lower_index:upper_index])
                        phrases.append(phrase)
            for sentence in sentences:
                print sentence, analyzer.sentiment(sentence), classifier.positivity(sentence), classifier.objectivity(sentence)
    """
    """
            for lst in extract_similar(phrases):
               print lst
            """

run()