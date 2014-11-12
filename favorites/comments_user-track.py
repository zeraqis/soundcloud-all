#!/usr/bin/env python
import csv
import ast

user_track_dict = {}
with open('track-user.tsv', 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter = '\t')
    for row in tsvreader:
        userlist = ast.literal_eval(row[1])
        for user in userlist:
            if user not in user_track_dict:
                user_track_dict[user] = []
            if row[0] not in user_track_dict[user]:
                user_track_dict[user].append(row[0])
with open('user-track.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    for user in user_track_dict:
        tsvwriter.writerow([user, user_track_dict[user]])