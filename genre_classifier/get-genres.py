#!/usr/bin/env python
import json
import csv
import cPickle as pickle
import yaml

track_genre_dict = {}
genres = []

with open('taxonomy.yaml', 'r') as yamlfile:
    yaml_genres = yaml.load(yamlfile)
    for genre in yaml_genres:
        genres.append(genre['key'])

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/genre_classifier/timed-comments-data.tsv', 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter = '\t')
    for row in tsvreader:
        if row[0] not in track_genre_dict:
            track_genres = row[-1].split(',')
            for track_genre in track_genres:
                if track_genre in genres:
                    track_genre_dict[row[0]] = track_genre

def assign_genres(timed_dict):
    count = 0
    for track in timed_dict:
        timed_dict[track]['genre'] = track_genre_dict[track]
        count += 1
    print count
    return timed_dict

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_train.json','r') as timed_train_json:
    timed_train_dict = json.load(timed_train_json)
    genre_train_dict = assign_genres(timed_train_dict)

with open('genre_train_dict.pickle', 'w') as genre_train_file:
    pickle.dump(genre_train_dict, genre_train_file)

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_dev.json','r') as timed_dev_json:
    timed_dev_dict = json.load(timed_dev_json)
    genre_dev_dict = assign_genres(timed_dev_dict)

with open('genre_dev_dict.pickle', 'w') as genre_dev_file:
    pickle.dump(genre_dev_dict, genre_dev_file)