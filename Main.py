from TextRank import key_phrases_for_course
from commentsearching import phrases_for_key_phrase, get_key_sentences
import sys
import re
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

"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_treebank_pos_tagger')
"""

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

    key_phrases = key_phrases_for_course(course, pos, window, custom_stop, min_keyword_len)
    if len(key_phrases) > 100:
        continue
    groups = []
    for key_phrase in key_phrases:
        phrases = phrases_for_key_phrase(key_phrase, course[1], 15)
        phrases = filter(lambda d: len(d) > 1, phrases)
        grps = analyzer.analyze(phrases)
        if len(grps) > 0:
            groups += grps
    final_groups = []
    sentences = []
    while True:
        max_length = 0
        group = None
        positivity = None
        for grp, pos in groups:
            length = len(grp)
            if length > max_length:
                max_length = length
                group = grp
                positivity = pos
        if group is None:
            break
        else:
            final_groups.append((group, positivity))
            groups.remove((group, positivity))
            for sentence in group:
                sentences.append(sentence)
                for grp, pos in groups:
                    for sentence2 in grp[:]:
                        if sentence == sentence2:
                            grp.remove(sentence)

    # auto summarization
    sentences_set = set(sentences)
    paragraph_sentences = []
    for i in range(0, 5):
        try:
            sentence = sentences_set.pop()
            sentence_stripped = sentence.strip()
            sentence_upper = sentence_stripped[0].upper() + sentence_stripped[1:]
            paragraph_sentences.append(sentence_upper)
        except KeyError:
            break

    pros = []
    cons = []

    for group in final_groups:
        phrases, sentiment = group
        if sentiment == 1:
            pros += [phrases]
        elif sentiment == -1:
            cons += [phrases]

    if (len(pros) is not 0) or (len(cons) is not 0):
        print course[0]
        if len(paragraph_sentences) > 0:
            print "Summary:", (". ".join(paragraph_sentences) + ".")
        print "Found %d key sentences" % len(sentences)

        if len(pros) > 0:
            print ""
            print "Pros:"
            for pro in pros:
                print "%s (in %d comment%s)" % (pro[0], len(pro), "s" if len(pro) > 1 else "")

        if len(cons) > 0:
            print ""
            print "Cons:"
            for con in cons:
                print "%s (in %d comment%s)" % (con[0], len(con), "s" if len(con) > 1 else "")

        print ""
        print "-------------------------------------------------------------------------------------------"
        print ""