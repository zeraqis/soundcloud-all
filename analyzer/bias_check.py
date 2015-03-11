#!/usr/bin/env python
import nltk
import os
import cPickle as pickle
import math
import csv
from preproc.filter import remove_diacritic
from xml.etree.ElementTree import XML

count = 0
terms = []
fd1 = nltk.FreqDist()
fd2 = nltk.FreqDist()
sub_dir = '/home/sathya/Dev/soundcloud-data/xml_original_final'
with open('track_ids.txt', 'rb') as txtfile:
    for line in txtfile:
        #print line
        flag = 0
        line = line.strip()
        with open('timed-comments-data.tsv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = '\t')
            for row in reader:
                if flag == 1:
                    break
                if line in row[0]:
                    fd1.inc(row[6])
                    terms = row[6].split(',')
                    for word in terms:
                        fd2.inc(word)
freq_tuples1 = fd1.items()
freq_tuples2 = fd2.items()
with open('combos.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '~')
    for item in freq_tuples1:
        writer.writerow(item)
with open('individual.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '~')
    for item in freq_tuples2:
        writer.writerow(item)