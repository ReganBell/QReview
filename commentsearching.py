'''
Matthew Beatty
CS51 Final Project
Q Comment Summarization
4/22/15
'''

# Import modules
import networkx as nx


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
        self._sentences_with_keywords = self._search_comments("CHEM 60: Foundations of Physical Chemistry",
                                                              ["both", "work", "exams", "math"])
        self.text = "test"


    def _search_comments(self, course_title, keyword_list):
        with open("2014QComments", "r") as raw:
            file_string = raw.read()

        courses = file_string.split("</course>")
        sentences_w_keywords = []
        for course in courses:
            title, comments_string = course.split("</title>")
            if (course_title == title):
                comments = comments_string.split("</comment>")
                for keyword in keyword_list:
                    sentences_w_keywords.append([sentence + '.' for sentence in comments.split('.') if keyword in comments])




cs = CommentSearching("fef", [])
cs._search_comments("fsda", [])