#!/usr/bin/env python
import nltk
import os
import cPickle as pickle
import math
import csv
from preproc.filter import remove_diacritic

sub_dir = '/home/sathya/Dev/soundcloud-data/categorized'
fd = nltk.FreqDist()
with open('drop_tracks.txt', 'rb') as txt:
    for line in txt:
        line = line.strip() + '.track'
        for root, dirs, files in os.walk(sub_dir):
                for filename in files:
                    if line in filename:
                        file_dir = os.path.join(root, filename)
                        with open(file_dir, 'rb') as input:
                            track = pickle.load(input)
                            file_index = int(math.ceil(track.comment_count/200))
                            if file_index == 0:
                                file_index = 1
                            for i in range(file_index):
                                comment_filename = str(track.id) + '_' + str(i+1) +'.comment'
                                comment_dir = os.path.join(root, comment_filename)
                                with open(comment_dir, 'rb') as comment_in:
                                    comments = pickle.load(comment_in)
                                    for comment in reversed(comments):
                                        sent = remove_diacritic(comment.body).lower()
                                        print sent
                                        for word in nltk.regexp_tokenize(sent, pattern=r'\.|(\s+)', gaps = True):
                                            fd.inc(word)
freq_tuples = fd.items()
with open('freq_punctv2.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '~')
    for item in freq_tuples:
        writer.writerow(item)
    