#!/usr/bin/env python
import os
import cPickle as pickle
import math
import datetime
import csv

date_format = "%Y/%m/%d"

sub_dir = 'D:/Dev/soundcloud data/final'

with open('relative_week.csv', 'wb') as csv_file:
    for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if 'track' in filename:
                date_list = []
                week_list = []
                week_count = -1
                comment_count = 0
                file_dir = os.path.join(root, filename)
                with open(file_dir, 'rb') as input:
                    track = pickle.load(input)
                    print track.created_at
                    print track.permalink_url
                    thresh_date = datetime.datetime.strptime(track.created_at.split()[0], date_format)
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
                                if comment.timestamp:
                                    comment_count += 1
                                    date, time, off = comment.created_at.split()
                                    date = datetime.datetime.strptime(date, date_format)
                                    print date, comment.timestamp
                                    if date < thresh_date + datetime.timedelta(days = 8):
                                        week_count += 1
                                    else:
                                        week_list.append(week_count + 1)
                                        thresh_date = date
                                        week_count = 0
                                    date_list.append(date)
                            if week_count:
                                week_list.append(week_count + 1)
                            if date == date_list[len(date_list) - 1] and date != date_list[len(date_list) - 2] and date == thresh_date:
                                week_list.append(1)
                                print "thresh", thresh_date
                for i_date in date_list:
                    print i_date
                if week_list[0]:
                    score1 = 1
                else:
                    score1 = 0
                score2 = 0
                for i in range(len(week_list)):
                    if i != len(week_list) - 1:
                        if week_list[i + 1] >= week_list[i] * 0.5:
                            score1 += 1
                    score2 += week_list[i] * (i + 1)
                for i in week_list:
                    print i
                print "score", score1, score2
                relDir = os.path.relpath(root, sub_dir)
                lic = str(relDir).split('\\')[0]
                genre = str(relDir).split('\\')[1]
                row = [track.id, track_genre, lic, genre, track.permalink_url, track.created_at, comment_count, score1, score2]
                writer = csv.writer(csv_file)
                writer.writerow(row)