#!/usr/bin/env python
import os
import cPickle as pickle
import math
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

sub_dir1 = '/home/sathya/Dev/soundcloud-data/categorized'
sub_dir2 = '/home/sathya/Dev/soundcloud-data/categorized_comments'
with open('relative_week.csv', 'rb') as track_file:
    reader = csv.reader(track_file)
    for row in reader:
        track_id = row[0]
        license = row[2]
        genre = row[3]
        root1 = sub_dir1 + '/' + license + '/' + genre
        root2 = sub_dir2 + '/' + license + '/' + genre
        if not os.path.exists(root2):
            os.makedirs(root2)
        csv_filename = track_id + '.csv'
        csv_dir = os.path.join(root2, csv_filename)
        track_filename = track_id + '.track'
        track_dir = os.path.join(root1, track_filename)
        with open(track_dir, 'rb') as track_input:
            track = pickle.load(track_input)
        file_index = int(math.ceil(track.comment_count/200))
        if file_index == 0:
            file_index = 1
        for i in range(file_index):
            comment_filename = str(track_id) + '_' + str(i+1) +'.comment'
            comment_dir = os.path.join(root1, comment_filename)
            with open(comment_dir, 'rb') as comment_in:
                comments = pickle.load(comment_in)
                for comment in reversed(comments):
                    if comment.timestamp:
                        try:
                            comment.body.decode('ascii')
                        except UnicodeEncodeError:
                            a = 1
                        else:
                            if len(comment.body) > 1 and 'http' not in comment.body and comment.user_id != track.user_id and '^' in comment.body:
                                print comment.body