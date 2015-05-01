from TextRank import key_phrases_for_course
import nltk
from commentsearching import phrases_for_key_phrase, get_key_sentences
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import Analyze

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

'''
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_treebank_pos_tagger')
'''
courses = parse_course_file("2014QComments")
positive = ["doable"]
negative = ["difficult", "hard", "work"]
analyzer = Analyze.SentimentAnalysis(positive, negative)

for course_num, course in enumerate(courses):

    # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
    # pos = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    pos = ["NN", "NNP", "NNPS", "NNS"]
    window = 2
    sentences = []
    custom_stop = ["course", "class", "this", "will", "in", "you", "make", "sure", "expect"]
    min_keyword_len = 4
    key_phrases = key_phrases_for_course(course, pos, window, custom_stop, min_keyword_len)[:5]
    key_sentences = set()

    for key_phrase in key_phrases:
        phrases = phrases_for_key_phrase(key_phrase, course[1], 12)
        sentences += get_key_sentences(key_phrase, course[1])
        for phrase in phrases:
            if len(phrase) > 1:
                key_sentences.add(phrase)


    groups = analyzer.analyze(list(key_sentences))

    # autosummarization
    paragraph = ""
    sentences_set = set(sentences[0:5])
    for sent in sentences_set:
        paragraph += (sent + " ")
    print paragraph

    pros = []
    cons = []

    for group in groups:
        phrases, sentiment = group
        if sentiment == 1:
            pros += [phrases]
        elif sentiment == -1:
            cons += [phrases]

    if len(pros) is not 0 and len(cons) is not 0:
        print course[0]
        print "Found %d key sentences" % len(key_sentences)

        print "Pros"
        for pro in pros:
            print "%s (in %d comment%s)" % (pro[0], len(pro), "s" if len(pro) > 1 else "")

        print "Cons"
        for con in cons:
            print "%s (in %d comment%s)" % (con[0], len(con), "s" if len(con) > 1 else "")


