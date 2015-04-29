'''
Matthew Beatty
CS51 Final Project
Q Comment Summarization
4/22/15
'''

# Import modules
import networkx as nx
from nltk import tokenize
import nltk


'''
We import the NetworkX library to use their DiGraph (directed graph) for our PageRank algorithm.

send in keywords, finds comments that match that
'''


class CommentSearching(object):

    '''
    Init Function
    '''

    def __init__(self, course_title, keyword_list):
        self._sentences_with_keywords = self._search_comments(course_title, keyword_list)


    def _search_comments(self, course_title, keyword_list):
        with open("2014QComments", "r") as raw:
            file_string = raw.read()

        courses = file_string.split("</course>")
        sentences_w_keywords = []

        del courses[-1]
        for course in courses:
            title, comments_string = course.split("</title>")
            if (course_title == title):
                raw_comments = comments_string.split("</comment>")
                # print (raw_comments)
                for comment in raw_comments:
                    comment_sentences = tokenize.sent_tokenize(comment)
                    for sentence in comment_sentences:
                        for keyword in keyword_list:
                            if keyword in sentence: sentences_w_keywords.append(sentence)

        print(sentences_w_keywords)


# cs = CommentSearching("CHEM 60: Foundations of Physical Chemistry", ["work", "exam"])