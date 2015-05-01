"""
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/30/15
"""

import re

contractions_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

b_incr = 2
b_decr = 0.5

degree_mod_dict = {"absolutely": b_incr, "amazingly": b_incr, "awfully": b_incr, "completely": b_incr, "considerably": b_incr,
                    "decidedly": b_incr, "deeply": b_incr, "effing": b_incr, "enormously": b_incr,
                    "entirely": b_incr, "especially": b_incr, "exceptionally": b_incr, "extremely": b_incr,
                    "fabulously": b_incr, "flipping": b_incr, "flippin": b_incr,
                    "fricking": b_incr, "frickin": b_incr, "frigging": b_incr, "friggin": b_incr, "fully": b_incr, "fucking": b_incr,
                    "greatly": b_incr, "hella": b_incr, "highly": b_incr, "hugely": b_incr, "incredibly": b_incr,
                    "intensely": b_incr, "majorly": b_incr, "more": b_incr, "most": b_incr, "particularly": b_incr,
                    "purely": b_incr, "quite": b_incr, "really": b_incr, "remarkably": b_incr,
                    "so": b_incr,  "substantially": b_incr,
                    "thoroughly": b_incr, "totally": b_incr, "tremendously": b_incr,
                    "uber": b_incr, "unbelievably": b_incr, "unusually": b_incr, "utterly": b_incr,
                    "very": b_incr,

                    "almost": b_decr, "barely": b_decr, "hardly": b_decr, "just enough": b_decr,
                    "kinda": b_decr, "kindof": b_decr, "kind-of": b_decr,
                    "less": b_decr, "little": b_decr, "marginally": b_decr, "occasionally": b_decr, "partly": b_decr,
                    "scarcely": b_decr, "slightly": b_decr, "somewhat": b_decr,
                    "sorta": b_decr, "sortof": b_decr, "sort-of": b_decr}

negate_list = ["arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
              "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
              "neednt", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
              "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent", "uh-uh",
              "without", "wont", "wouldnt", "rarely", "seldom", "despite"]

contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

def expand_contractions(word):
    """
    :type word: string
    :return: string: given word with contractions replaced
    """
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, word)

def modifier(word):
    """
    :type word: string
    :return: float: positivity change depending on intensity modifier and negation
    """
    if word in negate_list:
        return -1.0
    else:
        return degree_mod_dict.get(word, 1)