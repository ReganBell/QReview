'''
Matthew Beatty
CS51 Final Project
Q Comment Summarization
4/22/15
'''

# Import modules
import networkx as nx
from nltk import tokenize
from nltk.tokenize import wordpunct_tokenize
import nltk
import string


'''
We import the NetworkX library to use their DiGraph (directed graph) for our PageRank algorithm.

send in keywords, finds comments that match that
'''

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


def phrase_for_sentence(key_phrase, temp_list, pos_tag):
        for wp in temp_list:
            if wp.find(key_phrase) != -1:
                key_index = temp_list.index(wp)
            elif ('/' in key_phrase) or ('-' in key_phrase):
                #print key_phrase, temp_list
                key_index = temp_list.index(tsplit(key_phrase, (',', '.', '/', '-', '+'))[0])
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
                    #print temp_list
            else:
                try:
                    left = next(i for i, d in enumerate(pos_tag) if temp_list[0] in d)
                except StopIteration:
                    return None
                right = left + len(temp_list)
                pos_tag = pos_tag[left:right]
                try:
                    if pos_tag[wp_index][1] == 'CC':
                        #print pos_tag[wp_index][1], wordpunct, wp_index, key_index
                        if (wp_index < key_index) and ((temp_list[wp_index-1] == ',') or (temp_list[wp_index-1] == '.') or (temp_list[wp_index-1] == ':') or (temp_list[wp_index-1] == '!') or (temp_list[wp_index-1] == '?')):
                            temp_list = temp_list[(wp_index+1):]
                        elif (temp_list[wp_index-1] == ',') or (temp_list[wp_index-1] == '.') or (temp_list[wp_index-1] == ':') or (temp_list[wp_index-1] == '!') or (temp_list[wp_index-1] == '?'):
                            temp_list = temp_list[:wp_index]
                except IndexError:
                    return None
            # print temp_list
        if len(temp_list) <= 10:
            joined_contracted = ' '.join(temp_list).replace(' , ',',').replace(' .','.').replace(' !','!').replace(" ' ", "'")
            return joined_contracted.replace(' ?','?').replace(' : ',': ').replace(' \'', '\'')
        else:
            return None

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