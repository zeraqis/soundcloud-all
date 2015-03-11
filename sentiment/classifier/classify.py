#!/usr/bin/env python
import nltk
from featx import  allfeats

def nbclassify(sent, classifier):
   
    #test data
    temp = 'this is bad'
    label = classifier.classify(allfeats(sent,sent))
    
    return label