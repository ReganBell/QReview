'''
Matthew Beatty, Regan Bell, Akshay Saini
CS51 Final Project
Q Comment Summarization
4/22/15
'''

# Import modules
from nltk import tokenize
from nltk.tokenize import wordpunct_tokenize
import nltk


# Function for splitting string by specific delimiters
def tsplit(string, delimiters):

    delimiters = tuple(delimiters)
    stack = [string,]

    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)

    return stack


'''
phase_for_sentence extracts the keyphrase from the target sentence using part of speech tagging.
'''

def phrase_for_sentence(key_phrase, temp_list, pos_tag):
        # finds index of the keyphrase in the tokenized word list
        for wp in temp_list:
            if wp.find(key_phrase) != -1:
                key_index = temp_list.index(wp)
            elif ('/' in key_phrase) or ('-' in key_phrase):
                key_index = temp_list.index(tsplit(key_phrase, (',', '.', '/', '-', '+'))[0])

        # checks for punctuations and conjunctions to cut down tokenized word list
        for wp in temp_list:
            if wp in temp_list:
                wp_index = temp_list.index(wp)
            else:
                break
            if (wp == ',') or (wp == '.') or (wp == ':') or (wp == ';') or (wp == '!') or (wp == '?'):
                if wp_index < key_index:
                    temp_list = temp_list[wp_index:]
                else:
                    temp_list = temp_list[:wp_index]
            else:
                try:
                    left = next(i for i, d in enumerate(pos_tag) if temp_list[0] in d)
                except StopIteration:
                    return None
                right = left + len(temp_list)
                pos_tag = pos_tag[left:right]
                try:
                    if pos_tag[wp_index][1] == 'CC':
                        if (wp_index < key_index) and ((temp_list[wp_index-1] == ',') or (temp_list[wp_index-1] == '.') or (temp_list[wp_index-1] == ':') or (temp_list[wp_index-1] == '!') or (temp_list[wp_index-1] == '?')):
                            temp_list = temp_list[(wp_index+1):]
                        elif (temp_list[wp_index-1] == ',') or (temp_list[wp_index-1] == '.') or (temp_list[wp_index-1] == ':') or (temp_list[wp_index-1] == '!') or (temp_list[wp_index-1] == '?'):
                            temp_list = temp_list[:wp_index]
                except IndexError:
                    return None

        # final adjustments of keyphrase
        if (temp_list[0] == ',' or temp_list[0] == '.'):
            temp_list = temp_list[1:]
        if len(temp_list) <= 10:
            joined_contracted = ' '.join(temp_list).replace(' , ',',').replace(' .','.').replace(' !','!').replace(" ' ", "'")
            return joined_contracted.replace(' ?','?').replace(' : ',': ').replace(' \'', '\'')
        else:
            return None

'''
phrases_for_key_phrase looks through course comments for keywords and then compiles a list of
the keyphrases from those words.
'''

def phrases_for_key_phrase(key_phrase, comments):
        sentences = []
        for comment in comments:
            comment_sentences = tokenize.sent_tokenize(comment)
            for sentence in comment_sentences:
                tokenized = wordpunct_tokenize(unicode(sentence, errors='ignore'))
                if key_phrase in tokenized:
                    phrase = phrase_for_sentence(key_phrase, tokenized, nltk.pos_tag(tokenized))
                    if phrase is not None:
                        sentences.append(phrase)
        return sentences