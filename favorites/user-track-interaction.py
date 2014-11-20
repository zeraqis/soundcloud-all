#!/usr/bin/env python
from __future__ import division
import csv
import ast
import json

user_track_dict = {}
with open('comments_user-track.json', 'r') as user_track_file:
    plain_dict = json.load(user_track_file)
    for user in plain_dict:
        if user not in user_track_dict:
            user_track_dict[user] = {}
            user_track_dict[user]['commented'] = {}
            user_track_dict[user]['favorited'] = []
            user_track_dict[user]['stats'] = {}
            user_track_dict[user]['stats']['comment_and_favorite_list'] = []
            user_track_dict[user]['stats']['comment_and_not_favorite_list'] = []
        for  track in plain_dict[user]:
            if track not in user_track_dict[user]['commented']:
                user_track_dict[user]['commented'][track] = []
            user_track_dict[user]['commented'][track]= list(plain_dict[user][track])

with open('user-favorites.tsv', 'r') as user_favorite_file:
    user_track_reader = csv.reader(user_favorite_file, delimiter = '\t')
    for row in user_track_reader:
        favorite_tracklist = ast.literal_eval(row[1])
        user = row[0]
        for track in favorite_tracklist:
            user_track_dict[user]['favorited'].append(str(track))

for user in user_track_dict:
    commented = set(user_track_dict[user]['commented'])
    favorited = set(user_track_dict[user]['favorited'])
    user_track_dict[user]['stats']['comment_and_favorite_count'] = len(commented.intersection(favorited))
    user_track_dict[user]['stats']['comment_and_not_favorite_count'] = len(commented.difference(favorited))
    user_track_dict[user]['stats']['comment_and_favorite_list'] = list(commented.intersection(favorited))
    user_track_dict[user]['stats']['comment_and_not_favorite_list'] = list(commented.difference(favorited))
    user_track_dict[user]['stats']['comment_count'] = len(commented)
    user_track_dict[user]['stats']['favorite_count'] = len(favorited)
    user_track_dict[user]['stats']['percent'] = len(commented.intersection(favorited))/len(commented)*100
    

with open("user-interaction.json", "w") as json_file:
    json.dump(user_track_dict, json_file, indent=4)