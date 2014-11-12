#!/usr/bin/env python
import os
import cPickle as pickle
import csv

sub_dir = '/home/sathya/Dev/soundcloud-data/bulk_pickle'

track_user_dict = {}

for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            if 'comment' in filename:
                file_dir = os.path.join(root, filename)
                with open(file_dir, 'rb') as input:
                    comments = pickle.load(input)
                    for comment in reversed(comments):
                        if comment.track_id not in track_user_dict:
                            track_user_dict[comment.track_id] = []
                        track_user_dict[comment.track_id].append(comment.user_id)
print len(track_user_dict)
with open("track-user.tsv","w") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter="\t")
    for track in track_user_dict:
        csvwriter.writerow([track, track_user_dict[track]])