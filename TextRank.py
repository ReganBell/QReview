"""
Regan Bell, Akshay Saini, Matthew Beatty
CS51 Final Project
Q Comment Summarization
4/17/15
"""

# Import modules
import nltk
import plistlib
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import itertools
from operator import itemgetter
import networkx as nx
import os
from nltk.corpus import stopwords
from collections import defaultdict


def parse_course_file(path):

    with open(path, "r") as raw:
        file_string = raw.read()

    course_strings = file_string.split("</course>")
    courses = []

    for course_string in course_strings:
        if len(course_string) > 0:
            title, raw_comments = course_string.split("</title>")
            comments = raw_comments.split("</comment>")
            courses += [[title, comments]]

    return courses


def key_phrases_for_course(course, parts_of_speech, window, stop_words, min_keyword_length):

    phrase_dict = defaultdict(int)
    for comment in course[1]:
        phrases = find_key_phrases(comment, parts_of_speech, window, stop_words, min_keyword_length)
        for phrase in phrases: phrase_dict[phrase] += 1

    phrases = sorted(phrase_dict, key=phrase_dict.get, reverse=True)

    return phrases[0:(len(phrases) / 3) + 1]

def collapse_key_phrases(tokens, key_words):

    collapsed = []
    for j in range(1, len(tokens)):
        left = tokens[j-1]
        right = tokens[j]
        if left in key_words:
            while right in key_words:
                j += 1
                left += (' ' + right)
                right = [tokens[j] if j < len(tokens) else ""]
            collapsed += [left]
            j += 1
    return collapsed

def find_key_phrases(text, parts_of_speech, window, stop_words, min_keyword_length):

    tokens = nltk.word_tokenize(text)
    stop = stopwords.words('english')
    stop += stop_words
    filtered_tokens = [token for token in tokens if token not in stop and len(token) > min_keyword_length]
    tagged_tokens = nltk.pos_tag(filtered_tokens)
    vertices = set([])
    for i in range(0, len(tagged_tokens)):
        if tagged_tokens[i][1] in parts_of_speech:
            right = min(i + window, len(tagged_tokens))
            for j in range(i+1, right):
                vertex = (filtered_tokens[i], filtered_tokens[j], 1)

                vertices.add(vertex)

    gr = nx.Graph()
    gr.add_nodes_from(tokens)
    for (a, b, w) in vertices:
        gr.add_edge(a, b, weight=w)

    calculated_page_rank = nx.pagerank(gr, weight='weight')
    key_words = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)
    #collapsed = collapse_key_phrases(tokens, key_words)
    collapsed = key_words

    return [collapsed[0]] if len(collapsed) > 0 else []

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_treebank_pos_tagger')
courses = parse_course_file("2014QComments")
for course in courses:

    # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
    parts_of_speech = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    window = 2
    custom_stop_words = ["course", "class"]
    min_keyword_length = 2
    key_phrases = key_phrases_for_course(course, parts_of_speech, window, custom_stop_words, min_keyword_length)
    print key_phrases
