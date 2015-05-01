from TextRank import key_phrases_for_course
import nltk
from commentsearching import sentences_for_key_phrase
from TFIDFCalculator import TFIDFCalculator
import cProfile
import re
import

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

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_treebank_pos_tagger')
courses = parse_course_file("2014QComments")
for course in courses:

    # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
    pos = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    window = 2
    custom_stop = ["course", "class", "this", "will", "in", "you", "make", "sure", "expect"]
    min_keyword_len = 4
    #calc = TFIDFCalculator(courses)
    key_phrases = key_phrases_for_course(course, pos, window, custom_stop, min_keyword_len)
    for key_phrase in key_phrases:
        sentences = sentences_for_key_phrase(key_phrase, course[1])
        print sentences

    print course[0]
    print key_phrases
