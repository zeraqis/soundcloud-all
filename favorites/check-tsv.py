#!/usr/bin/env python
import os
import cPickle as pickle
import csv

sub_dir = '/home/sathya/Dev/soundcloud-data/bulk_pickle'

tsv_tracks = []
pickle_tracks = []
with open("track-user.tsv","r") as csvfile:
    csvreader = csv.reader(csvfile, delimiter = '\t')
    for row in csvreader:
        tsv_tracks.append(row[0])
for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if '_1.comment' in filename:
                pickle_tracks.append(filename.split('_1.comment')[0])
a = set(tsv_tracks)
b = set(pickle_tracks)
print len(a)
print len(b)
print b.difference(a)
print a.difference(b)