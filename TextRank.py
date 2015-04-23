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

class TextRank(object):

    def __init__(self, comments, windowSize, granularity, partsOfSpeech):
        print "New TextRank created"



with open("2014QComments", "r") as raw:
    file_string = raw.read()
    nltk.help.upenn_tagset()

courses = file_string.split("</course>")
for course in courses:
    title, comments_string = course.split("</title>")
    print title
    comments = comments_string.split("</comment>")
    # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
    parts_of_speech = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    text_rank = TextRank(comments, 2, 1, parts_of_speech)



