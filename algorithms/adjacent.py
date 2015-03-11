#!/usr/bin/env python
import os
import cPickle as pickle
import math
from datetime import datetime
import csv

date_format = "%Y/%m/%d"

sub_dir = 'D:/Dev/soundcloud data/final'

with open('adjacent.csv', 'wb') as csv_file:
    for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if 'track' in filename:
                date_list = []
                diff_list = []
                comment_count = 0
                file_dir = os.path.join(root, filename)
                with open(file_dir, 'rb') as input:
                    track = pickle.load(input)
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
                            for comment in comments:
                                if comment.timestamp:
                                    comment_count += 1
                                    date, time, off = comment.created_at.split()
                                    print date
                                    date_list.append(datetime.strptime(date, date_format))
                for i in range(len(date_list)):
                    if i!= 0:
                        diff = abs(date_list[i] - date_list[i-1])
                        diff_list.append(diff)
                diff_list.sort()
                max_diff = max(date_list) - min(date_list)
                max_adj_diff = diff_list[len(diff_list) - 1] - diff_list[0]
                if max_adj_diff.days == 0:
                    score = 0
                else:
                    score = float(max_diff.days/max_adj_diff.days)
                row = [track.id, track_genre, track.permalink_url, track.created_at, comment_count, score]
                writer = csv.writer(csv_file)
                writer.writerow(row)
