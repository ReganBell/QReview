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


def sentences_for_key_phrase(key_phrase, comments):

    for comment in comments:
        comment_sentences = tokenize.sent_tokenize(comment)
        for sentence in comment_sentences:
            if key_phrase in sentence: # sentences_w_keywords.append(sentence)
                temp_list = wordpunct_tokenize(sentence)
                for wordpunct in temp_list:
                    for wp in temp_list:
                        if wp.find(key_phrase) != -1:
                            key_index = temp_list.index(wp)
                        elif ' ' or '/' or '-' in key_phrase:
                            key_index = temp_list.index(key_phrase.split( )[0])
                    print wordpunct, temp_list
                    if temp_list.__contains__(wordpunct):
                        wp_index = temp_list.index(wordpunct)
                    else:
                        break
                    if wordpunct == ',' or '.' or ':' or ';' or '!' or '?':
                        if wp_index < key_index:
                            temp_list = temp_list[wp_index:]
                        else:
                            temp_list = temp_list[:wp_index]
                            print temp_list
                    else:
                        pos_tag = nltk.pos_tag(temp_list)
                        if pos_tag[wp_index][1] == 'CC':
                            print pos_tag[wp_index][1], wordpunct, wp_index, key_index
                            if (wp_index < key_index and temp_list[wp_index-1] == (',' or '.' or ':' or '!' or '?')):
                                temp_list = temp_list[(wp_index+1):]
                            elif (temp_list[wp_index-1] == (',' or '.' or ':' or '!' or '?')):
                                temp_list = temp_list[:wp_index]
                    # print temp_list
                print(temp_list)