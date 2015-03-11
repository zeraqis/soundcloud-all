#!/usr/bin/env python
import json
import csv

def analyze_json(json, string):
    user_count = 0
    track_count = 0
    comment_count = 0
    for track in json:
        track_count += 1
        for user in json[track]:
            user_count += 1
            for comment in list(json[track][user]):
                comment_count += 1
    return [string, user_count, track_count, comment_count]

with open('analyze_split.tsv','w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter = '\t')
    tsvwriter.writerow(['set', 'user_count', 'track_count', 'comment_count'])
    
    with open('timed_train.json', 'r') as train_json:
        train_dict = json.load(train_json)
        tsvwriter.writerow(analyze_json(train_dict, 'train'))
    
    with open('timed_dev.json', 'r') as dev_json:
        dev_dict = json.load(dev_json)
        tsvwriter.writerow(analyze_json(dev_dict, 'dev'))