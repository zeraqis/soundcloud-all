#!/usr/bin/env python
import csv
import ast
import json

user_track_dict = {}
with open('comments_track-user.json', 'r') as json_file:
    track_user_dict = json.load(json_file)
    for track in track_user_dict:
        userlist = list(track_user_dict[track])
        for user in userlist:
            if user not in user_track_dict:
                user_track_dict[user] = {}
            if track not in user_track_dict[user]:
                user_track_dict[user][track] = []
            for comment in track_user_dict[track][user]:
                user_track_dict[user][track].append(comment)

with open('comments_user-track.json', 'w') as new_json_file:
    json.dump(user_track_dict, new_json_file, indent = 4)