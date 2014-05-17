#!/usr/bin/env python
from nltk.corpus import movie_reviews
from reader.csv_reader import preproc
from reader.csv_reader import readcsv
from reader.csv_reader import writecsv
from classifier.classify import nbclassify
from classifier.featx import  allfeats
import os
import shutil
import nltk

sub_dir = 'D:/Dropbox/Work/Sound Cloud/Data/train/dubstep'
sub_dir2 = 'D:/Dropbox/Work/Sound Cloud/Data/train/dubstep/new'
sub_dir3 = 'D:/Dropbox/Work/Sound Cloud/Data/train/dubstep/lab'
if os.path.exists(sub_dir2):
    shutil.rmtree(sub_dir2)
if os.path.exists(sub_dir3):
    shutil.rmtree(sub_dir3)

for filename in os.listdir(sub_dir):
    preproc(sub_dir, sub_dir2, filename)

#movie review data to train
documents = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]

#feat extraction for train
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]
featuresets = [(allfeats(d, word_features), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]

#classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

for filename in os.listdir(sub_dir2):
    row = readcsv(sub_dir2, filename)
    #print row[1]
    nrow = [row[0], row[1], nbclassify(row[1], classifier)]
    print nrow
    writecsv(sub_dir2, sub_dir3, filename, nrow)