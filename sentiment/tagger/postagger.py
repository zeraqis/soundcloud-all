#!/usr/bin/env python
import nltk

verbs = {'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
adj = {'JJ', 'JJR', 'JJS', 'JJT'}
nouns = {'NN', 'NN$', 'NNS', 'NNS$', 'NP', 'NP$', 'NPS', 'NPS$', 'NR'}
adv = {'RB', 'RBR', 'RBT', 'RN', 'RP'}

def brown_tag(string):
    tokens = nltk.word_tokenize(string)
    tags = nltk.pos_tag(tokens)
    return tags

def tag_index(tags):
    stag = []
    for tag in tags:
        if tag[1] in verbs:
            stag.append([tag[0], 'v'])
        elif tag[1] in adj:
            stag.append([tag[0], 'a'])
        elif tag[1] in nouns:
            stag.append([tag[0], 'n'])
        elif tag[1] in adv:
            stag.append([tag[0], 'r'])
        else:
            stag.append(tag)
    return stag