from TextRank import key_phrases_for_course
import nltk


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
    parts_of_speech = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    window = 2
    custom_stop_words = ["course", "class", "this", "will", "in", "you", "make", "sure", "expect"]
    min_keyword_length = 4
    key_phrases = key_phrases_for_course(course, parts_of_speech, window, custom_stop_words, min_keyword_length)
    print course[0]
    print key_phrases
