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
from pagerank import pagerank

def lowercase_tokenize(string):

    raw_tokens = nltk.word_tokenize(string)
    return [token.lower() for token in raw_tokens]

def find_key_phrases(tokens, parts_of_speech, window):

    tagged_tokens = nltk.pos_tag(tokens)
    vertices = []
    for i in range(0, len(tagged_tokens)):
        if tagged_tokens[i][1] in parts_of_speech:
            right = min(i + window, len(tagged_tokens))
            for j in range(i+1, right):
                vertex = (tokens[i], tokens[j], {"weight": 1})
                vertices += [vertex]
    return pagerank(vertices, 0.15, 100)


def key_phrases_for_course(course, parts_of_speech, window, stop_words, min_keyword_length):

    words = {}
    all_tokens = []
    stop = stopwords.words('english')
    stop += stop_words

    for comment in course[1]:
        tokens = lowercase_tokenize(comment)
        filtered_tokens = [token for token in tokens if (token not in stop and len(token) >= min_keyword_length)]
        all_tokens += tokens
        new = find_key_phrases(filtered_tokens, parts_of_speech, window)
        words.update(new)

    sorted_words = sorted(words, key=words.get, reverse=True)
    top_third_words = sorted_words[0:(len(sorted_words) / 3) + 1]
    top_words_dict = {}
    for word in top_third_words:
        top_words_dict.update({word: words[word]})
    phrases = collapse_key_phrases(all_tokens, top_words_dict)

    return sorted(phrases, key=words.get, reverse=True)


def collapse_key_phrases(tokens, key_words):

    collapsed = {}
    for j in range(1, len(tokens)):
        left = tokens[j-1]
        right = tokens[j]
        if left in key_words:
            combined_score = key_words[left]
            while right in key_words:
                j += 1
                left += (' ' + right)
                combined_score += key_words[right]
                right = tokens[j] if j < len(tokens) else ""
            collapsed.update({left: combined_score})
            j += 1
    return collapsed