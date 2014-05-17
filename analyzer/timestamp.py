#!/usr/bin/env python
import csv
import os
import math
import cPickle as pickle

sub_dir = 'D:/Dev/soundcloud data/bulk'
final = []
for root, dirs, files in os.walk(sub_dir):
    for file in files:
        if 'track' in file:
            file_dir = os.path.join(root,file)
            with open(file_dir, 'rb') as input:
                track = pickle.load(input)
                print track.comment_count
#with open('refined.csv', 'rb') as csv_file:
#    reader = csv.reader(csv_file)
#    for row in reader:
#        timestamp = 0
#        track_id = row[5]
#        no_comments = int(row[6])
#        
#                        with open(comment_dir, 'rb') as input:
#                            comments = pickle.load(input)
#                            for comment in comments:
#                                if comment.timestamp:
#                                    timestamp += 1
#        row.append(timestamp)
#        final.append(row)
#with open('final.csv', 'wb') as csv_file:
#    writer = csv.writer(csv_file)
#    for row in final:
#        writer.writerow(row)
