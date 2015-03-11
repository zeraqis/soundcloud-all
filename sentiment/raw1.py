#!/usr/bin/env python
from sentiment.swnreader import SWNReader
from preproc.spell_check import correct

swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
swn = SWNReader(swn_filename)
try:
    pos, neg = swn.no_pos_senti_synset('awesome')
    print pos, neg
except TypeError:
    print "None found"
try:
    pos, neg = swn.senti_synset('awesome.a.1')
    print pos, neg
except TypeError:
    print "None found"
try:
    synset = swn.synset('awesome')
    print synset
except TypeError:
    print "None found"
    
print correct('heppy')