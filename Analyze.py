"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/16/15
"""

import re
from nltk.stem.snowball import EnglishStemmer
import math
import Classifier
from nltk.corpus.reader.wordnet import Lemma
from nltk.corpus import wordnet as wn

word_similarity_method = 1  # 0 or 1 or 2
sentiment_analysis_method = 0  # 0 or 1

# helper methods for sentence similarity


def vector_operator(vector1, vector2, operator):
    """
    :type vector1: float list
    :type vector2: float list
    :type operator: function (float -> float -> float)
    :return: vector, each element of which is the operator applied to corresponding elements of the given vectors
    """
    to_return = []
    for i in range(0, len(vector1)):
        to_return.append(operator(vector1[i], vector2[i]))
    return to_return


def vector_sum(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: vector, which is the vector sum of the given vectors
    """
    return vector_operator(vector1, vector2, lambda a, b: a + b)


def vector_diff(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: vector, which is the vector difference of the given vectors
    """
    return vector_operator(vector1, vector2, lambda a, b: a - b)


def dot_product(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float, which is the dot product of the given vectors
    """
    to_return = 0
    for i in range(0, len(vector1)):
        to_return += vector1[i] * vector2[i]
    return to_return


def vector_length(vector):
    """
    :type vector: float list
    :return: float, which is the length of the given vector
    """
    return math.sqrt(dot_product(vector, vector))


def cosine_similarity(vector1, vector2):
    """
    :type vector1: float list
    :type vector2: float list
    :return: float between 0 and 1, which is the cosine of the angle between the given vectors
    """
    return dot_product(vector1, vector2) / (vector_length(vector1) * vector_length(vector2))


def case_1(word1, word2):
    """
    :type word1: string
    :type word2: string
    :return: Boolean, which is True if the words are in the same WordNet Synset
    """
    concepts1 = wn.synsets(word1)
    concepts2 = wn.synsets(word2)
    for concept1 in concepts1:
        for concept2 in concepts2:
            if concept1 == concept2:
                return True
    return False


def case_2(word1, word2):
    """
    :type word1: string
    :type word2: string
    :return: Boolean, which is True if there is a common word in each of the word's WordNet Synsets
    """
    concepts1 = wn.synsets(word1)
    concepts2 = wn.synsets(word2)
    for concept1 in concepts1:
        for concept2 in concepts2:
            words1 = map(Lemma.name, concept1.lemmas())
            words2 = map(Lemma.name, concept2.lemmas())
            for word1 in words1:
                for word2 in words2:
                    if word1 == word2:
                        return True
    return False


def get_path_length(word1, word2):
    """ see section 2.3 of http://dx.doi.org.ezp-prod1.hul.harvard.edu/10.1109/TKDE.2003.1209005
    :type word1: string
    :type word2: string
    :return: float, which is the path length between the given words, using the WordNet tree
    """
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
                    shortest_path = path_length if (shortest_path is None) or (path_length < shortest_path) else shortest_path
        return shortest_path if shortest_path is not None else 0

def get_subsumer_height(word1, word2):
    """ see section 2.4 of http://dx.doi.org.ezp-prod1.hul.harvard.edu/10.1109/TKDE.2003.1209005
    :type word1: string
    :type word2: string
    :return: float, which is the depth (WordNet hierarchy) of the subsumer along the shortest path between given words
    """
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

def get_path_length_and_subsumer_height(word1, word2):
    """ see section 2.3 of http://dx.doi.org.ezp-prod1.hul.harvard.edu/10.1109/TKDE.2003.1209005
    :type word1: string
    :type word2: string
    :return: (float, float), where the first is the path length between the given words, and the second is the depth of the subsumer along that path
    """
    concepts1 = wn.synsets(word1)
    concepts2 = wn.synsets(word2)
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


def similarity_score0(word1, word2):
    alpha = 0.2
    beta = 0.6
    l = get_path_length(word1, word2)
    h = get_subsumer_height(word1, word2)
    return math.exp((-1)*alpha*l)*((math.exp(beta*h)-math.exp((-1)*beta*h))/(math.exp(beta*h)+math.exp((-1)*beta*h)))

def similarity_score1(word1, word2):
    """
    :param word1: string (word)
    :param word2: string (word)
    :return: string as section 2.2 of https://www.aaai.org/Papers/FLAIRS/2004/Flairs04-139.pdf
    """
    alpha = 0.2
    beta = 0.45
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    highest_score = 0
    for synset1 in synsets1:
        for synset2 in synsets2:
            l = synset1.shortest_path_distance(synset2)
            subsumers = synset1.lowest_common_hypernyms(synset2)
            score = 0
            for subsumer in subsumers:
                h = subsumer.max_depth()
                score=math.exp((-1)*alpha*l)*(math.exp(beta*h)-math.exp((-1)*beta*h))/(math.exp(beta*h)+math.exp((-1)*beta*h))
            if score > highest_score:
                highest_score = score
    return highest_score

def similarity_score2(word1, word2):
    alpha = 0.2
    beta = 0.6
    l, h = get_path_length_and_subsumer_height(word1, word2)
    return math.exp((-1)*alpha*l)*((math.exp(beta*h)-math.exp((-1)*beta*h))/(math.exp(beta*h)+math.exp((-1)*beta*h)))

def semantic_vector_element(word, words, threshold):
    if word in words:
        return 1
    else:
        highest_score = 0
        for word1 in words:
            if word_similarity_method == 0:
                score = similarity_score0(word, word1)
            elif word_similarity_method == 1:
                score = similarity_score1(word, word1)
            else:
                score = similarity_score2(word, word1)
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
    semantic_vector1, semantic_vector2 = [], []
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
            similarity = similarity_score0(word, word1)
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
    words1, words2 = re.split("[\W]", sentence1), re.split("[\W]", sentence2)
    all_words = set(words1).union(set(words2))
    order_vector1, order_vector2 = [], []
    for word in all_words:
        order_vector1.append(index_in(word, words1, threshold))
        order_vector2.append(index_in(word, words2, threshold))
    return normalized_difference(order_vector1, order_vector2)

# sentence similarity

def sentence_similarity(sentence1, sentence2):
    semantic_threshold = 0.2
    order_threshold = 0.4
    semantic_weight = 0.85
    semantic = semantic_similarity(sentence1, sentence2, semantic_threshold)
    order = word_order_similarity(sentence1, sentence2, order_threshold)
    similarity = semantic_weight * semantic + (1 - semantic_weight) * order
    return similarity


# sentiment analysis
class SentimentAnalysis:
    def __init__(self):
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

    def sentiment(self, sentence):
        tokens = re.split("[\W]",sentence)
        polarity = 0
        stemmer = EnglishStemmer()
        for word in tokens:
            stemmed = stemmer.stem(word)
            polarity += self.dictionary.get(stemmed, 0)
        return polarity


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
    sentence1 = "The quick brown fox jumps over the lazy dog"
    sentence2 = "The fast tan coyote leaps above the sluggish canine"
    print "sentence similarity: {0:.3f}".format(sentence_similarity(sentence1, sentence2))

    classifier = Classifier.Classifier()
    analyzer = SentimentAnalysis()
    print 'subjectivity: {0:.2f}, analyzer positivity: {1}, classifier positivity: {2:.2f}'.format(classifier.subjectivity(sentence1), analyzer.sentiment(sentence1), classifier.positivity(sentence1))

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