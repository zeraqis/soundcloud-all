#!/usr/bin/env python
import os
import cPickle as pickle
import csv
import json

sub_dir = '/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/bulk_pickle'

track_user_dict = {}

for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if 'comment' in filename:
                file_dir = os.path.join(root, filename)
                with open(file_dir, 'rb') as input:
                    comments = pickle.load(input)
                    for comment in reversed(comments):
                        if comment.track_id not in track_user_dict:
                            track_user_dict[comment.track_id] = {}
                        if comment.user_id not in track_user_dict[comment.track_id]:
                                track_user_dict[comment.track_id][comment.user_id] = []
                        track_user_dict[comment.track_id][comment.user_id].append(comment.body)
print len(track_user_dict)

with open("comments_track-user-temp.json","w") as json_file:
    json.dump(track_user_dict, json_file, indent=4)