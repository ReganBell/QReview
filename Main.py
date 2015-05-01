from TextRank import key_phrases_for_course
import nltk
from commentsearching import phrases_for_key_phrase
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


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_treebank_pos_tagger')

courses = parse_course_file("2014QComments")
analyzer = Analyze.SentimentAnalysis()

for course_num, course in enumerate(courses):

    # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
    pos = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    window = 2
    custom_stop = ["course", "class", "this", "will", "in", "you", "make", "sure", "expect"]
    min_keyword_len = 4
    key_phrases = key_phrases_for_course(course, pos, window, custom_stop, min_keyword_len)
    print course_num, course[0]
    groups = []
    for key_phrase in key_phrases:
        phrases = phrases_for_key_phrase(key_phrase, course[1])
        phrases = filter(lambda d: len(d) > 1, phrases)
        grps = analyzer.analyze(phrases)
        if len(grps) > 0:
            groups += grps
    final_groups = []
    while True:
        max_length = 0
        group = None
        positivity = None
        for grp, pos in groups:
            length = len(grp)
            if length > max_length:
                max_length =length
                group = grp
                positivity = pos
        if group is None:
            break
        else:
            final_groups.append((group, positivity))
            groups.remove((group, positivity))
            for sentence in group:
                for grp, pos in groups:
                    for sentence2 in grp[:]:
                        if sentence == sentence2:
                            grp.remove(sentence)

    pros = []
    cons = []
    neutrals = []

    for group in final_groups:
        phrases, sentiment = group
        if sentiment == 1:
            pros += [phrases]
        elif sentiment == -1:
            cons += [phrases]
        """
        else:
            neutrals += [phrases]
        """

    print "Pros"
    for pro in pros:
        print "%s (in %d comment%s)" % (pro[0], len(pro), "s" if len(pro) > 1 else "")


    print "Cons"
    for con in cons:
        print "%s (in %d comment%s)" % (con[0], len(con), "s" if len(con) > 1 else "")

    print ""
"""
    print "Neutral"
    for neutral in neutrals:
        print "%s (in %d comment%s)" % (neutral[0], len(neutral), "s" if len(neutral) > 1 else "")
"""
