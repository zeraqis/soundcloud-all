#!/usr/bin/env python
import json

user_track_dict = {}
with open('comments_track-user-timed.json','r') as json_file:
    track_user_dict = json.load(json_file)
    for track in track_user_dict:
        userlist = list(track_user_dict[track])
        for user in userlist:
            if user not in user_track_dict:
                user_track_dict[user] = {}
            if track not in user_track_dict[user]:
                user_track_dict[user][track] = {}
            for time in track_user_dict[track][user]:
                user_track_dict[user][track][time] = track_user_dict[track][user][time]

with open('comments_user-track-timed.json', 'w') as new_json_file:
    json.dump(user_track_dict, new_json_file, indent = 4)