#!/usr/bin/env python
import os
import cPickle as pickle
import math
import csv
from preproc.filter import remove_diacritic
import nltk

sub_dir = '/home/sathya/Dev/soundcloud-data/categorized'
fd = nltk.FreqDist()
for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if 'track' in filename:
                file_dir = os.path.join(root, filename)
                with open(file_dir, 'rb') as input:
                    track = pickle.load(input)
                    for ch in remove_diacritic(track.title):
                        if ch == chr(127):
                            print track.permalink_url
                            print track.title, 'title'
                        fd.inc(ch)
                    for ch in remove_diacritic(track.description):
                        if ch == chr(127):
                            print track.permalink_url
                            print track.description, 'description'
                        fd.inc(ch)
                    for ch in remove_diacritic(track.label_name):
                        if ch == chr(127):
                            print track.permalink_url
                            print track.label_name, 'label_name'
                        fd.inc(ch)
                    for ch in remove_diacritic(track.release):
                        if ch == chr(127):
                            print track.permalink_url
                            print track.release, 'release'
                        fd.inc(ch)
                    #print thresh_date, track.created_at
                    if not(track.genre):
                        track_genre = 'None'
                    else:
                        track_genre = track.genre.encode("utf-8")
                    file_index = int(math.ceil(track.comment_count/200))
                    if file_index == 0:
                        file_index = 1
                    for i in range(file_index):
                        comment_filename = str(track.id) + '_' + str(i+1) +'.comment'
                        comment_dir = os.path.join(root, comment_filename)
                        with open(comment_dir, 'rb') as comment_in:
                            comments = pickle.load(comment_in)
                            for comment in reversed(comments):
                                for ch in remove_diacritic(comment.body):
                                    if ch == chr(127):
                                        print track.permalink_url
                                        print 'comment.body'
                                    fd.inc(ch)
                                for ch in remove_diacritic(comment.user['username']):
                                    if ch == chr(127):
                                        print track.permalink_url
                                        print comment.user['username'], 'username'
                                    fd.inc(ch)
freq_tuples = fd.items()
with open('char.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '~')
    for item in freq_tuples:
        writer.writerow(item)