#!/usr/bin/env python

from sentiment.swnreader import SentiWordNetCorpusReader, SentiSynset
from tagger.postagger import brown_tag
from tagger.postagger import tag_index

allstags = {'a', 'r', 'v', 'n'}

swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)

text = "she is awesome"
tags = brown_tag(text)
print tags

stags = tag_index(tags)

for i,stag in enumerate(stags):
    if stag[1] not in allstags:
        #print stags[i]
        sentisynsets = swn.senti_synsets(stag[0])
        
        for sentisynset in sentisynsets:
            temp = sentisynset.synset.name.split('.')[1]
            stags[i] = [stag[0], temp]
print stags

curr_synsets = []
all_synsets = []

for stag in stags:
    if stag[1] in allstags:
        curr_synsets.append((stag[0] + '.' + stag[1] + '.' + '01'))

print curr_synsets

swn2 = SentiWordNetCorpusReader(swn_filename)

for syn in swn2.all_senti_synsets():
    all_synsets.append(syn.synset.name)

for i in range(0,10):
    print all_synsets[i]