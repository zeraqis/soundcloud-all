#!/usr/bin/env python
import os
import cPickle as pickle
import math
import datetime
import csv

date_format = "%Y/%m/%d"

sub_dir = 'D:/Dev/soundcloud data/final'

with open('first_week.csv', 'wb') as csv_file:
    for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if 'track' in filename:
                date_list = []
                diff_list = []
                comment_count = 0
                week_count = 0
                file_dir = os.path.join(root, filename)
                with open(file_dir, 'rb') as input:
                    track = pickle.load(input)
                    print track.created_at
                    track_date = datetime.datetime.strptime(track.created_at.split()[0], date_format)
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
                                    date = datetime.datetime.strptime(date, date_format)
                                    if date < track_date + datetime.timedelta(days = 8):
                                        week_count += 1
                                    date_list.append(date)
                if week_count == 0:
                    score = 0
                else:
                    score = float(comment_count/week_count)
                row = [track.id, track_genre, track.permalink_url, track.created_at, comment_count, score]
                writer = csv.writer(csv_file)
                writer.writerow(row)
