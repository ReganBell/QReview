from TextRank import key_phrases_for_course
import nltk
from commentsearching import sentences_for_key_phrase
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from Analyze import analyze

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
for course in courses[10:11]:

    # Nouns and adjectives, run nltk.help.upenn_tagset() to see all possible tags
    pos = ["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]
    window = 2
    custom_stop = ["course", "class", "this", "will", "in", "you", "make", "sure", "expect"]
    min_keyword_len = 4
    key_phrases = key_phrases_for_course(course, pos, window, custom_stop, min_keyword_len)
    print course[0]
    key_sentences = []
    for key_phrase in key_phrases:
        sentences = sentences_for_key_phrase(key_phrase, course[1])
        groups = analyze(key_phrase, sentences[0:5])
        if len(groups) > 0:
            key_sentences += groups

    pros = []
    cons = []
    neutrals = []

    for group in key_sentences:
        sentences, sentiment = group
        if sentiment == 1:
            pros += [sentences]
        elif sentiment == -1:
            cons += [sentences]
        else:
            neutrals += [sentences]

    print "Pros"
    for pro in pros:
        print "%s (in %d comment%s)" % (pro[0], len(pro), "s" if len(pro) > 1 else "")


    print "Cons"
    for con in cons:
        print "%s (in %d comment%s)" % (con[0], len(con), "s" if len(con) > 1 else "")


    print "Neutral"
    for neutral in neutrals:
        print "%s (in %d comment%s)" % (neutral[0], len(neutral), "s" if len(neutral) > 1 else "")
