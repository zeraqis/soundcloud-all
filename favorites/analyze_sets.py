#!/usr/bin/env python
import json
import csv

def analyze_json(json, string):
    user_count = 0
    track_count = 0
    comment_count = 0
    for user in json:
        user_count += 1
        for track in json[user]:
            track_count += 1
            for comment in list(json[user][track]):
                comment_count += 1
    return [string, user_count, track_count, comment_count]

with open('analyze_sets.tsv','w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter = '\t')

    with open('train_favorite-comments.json','r') as json_file:
        train_favorite_comments_json = json.load(json_file)
        tsvwriter.writerow(analyze_json(train_favorite_comments_json, 'train_favorite'))

    with open('train_not_favorite-comments.json','r') as json_file:
        train_not_favorite_comments_json = json.load(json_file)
        tsvwriter.writerow(analyze_json(train_not_favorite_comments_json, 'train_not_favorite'))
    
    with open('test_favorite-comments.json','r') as json_file:
        test_favorite_comments_json = json.load(json_file)
        tsvwriter.writerow(analyze_json(test_favorite_comments_json, 'test_favorite'))
    
    with open('test_not_favorite-comments.json','r') as json_file:
        test_not_favorite_comments_json = json.load(json_file)
        tsvwriter.writerow(analyze_json(test_not_favorite_comments_json, 'test_not_favorite'))

    with open('dev_favorite-comments.json','r') as json_file:
        dev_favorite_comments_json = json.load(json_file)
        tsvwriter.writerow(analyze_json(dev_favorite_comments_json, 'dev_favorite'))
    
    with open('dev_not_favorite-comments.json','r') as json_file:
        dev_not_favorite_comments_json = json.load(json_file)
        tsvwriter.writerow(analyze_json(dev_not_favorite_comments_json, 'dev_not_favorite'))