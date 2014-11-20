#!/usr/bin/env python
import cPickle as pickle
import json
import os

sub_dir = '/home/sathya/Dev/soundcloud-data/bulk_pickle'
curr_tracks = []
train_favorited_comments = {}
train_not_favorited_comments = {}
test_favorited_comments = {}
test_not_favorited_comments = {}
dev_favorited_comments = {}
dev_not_favorited_comments = {}

with open('comment-favorite_user-track.json', 'r') as track_json_file:
    fav_user_tracks = json.load(track_json_file)

with open('comment-not-favorite_user-track.json', 'r') as not_track_json_file:
    not_fav_user_tracks = json.load(not_track_json_file)

with open('user-interaction.json', 'r') as interaction_json_file:
    interactions = json.load(interaction_json_file)

def create_set(users):
    json = {}
    not_json = {}
    for user in users:
        user = user.strip()
        curr_tracks = list(fav_user_tracks[user])
        not_curr_tracks = list(not_fav_user_tracks[user])
        for track in curr_tracks:
            for comment in list(interactions[user]['commented'][track]):
                print comment
                comment = comment.strip()
                if len(comment) > 0 and comment != "":
                    if user not in json:
                        json[user] = {}
                    if track not in json[user]:
                        json[user][track] = []
                    json[user][track].append(comment)
        for track in not_curr_tracks:
            for comment in list(interactions[user]['commented'][track]):
                print comment
                comment = comment.strip()
                if len(comment) > 0 and comment != "":
                    if user not in not_json:
                        not_json[user] = {}
                    if track not in not_json[user]:
                        not_json[user][track] = []
                    not_json[user][track].append(comment)
    return json, not_json


#with open('train_users.txt', 'r') as train_file:
#    users = train_file.readlines()
#    train_favorited_comments, train_not_favorited_comments  = create_set(users)
#    with open('train_favorite-comments.json','w') as new_json_file:
#        json.dump(train_favorited_comments, new_json_file, indent = 4)
#    with open('train_not_favorite-comments.json','w') as new_json_file:
#        json.dump(train_not_favorited_comments, new_json_file, indent = 4)
#
#
#with open('test_users.txt', 'r') as test_file:
#    users = test_file.readlines()
#    test_favorited_comments, test_not_favorited_comments  = create_set(users)
#    with open('test_favorite-comments.json','w') as new_json_file:
#        json.dump(test_favorited_comments, new_json_file, indent = 4)
#    with open('test_not_favorite-comments.json','w') as new_json_file:
#        json.dump(test_not_favorited_comments, new_json_file, indent = 4)

with open('dev_users.txt', 'r') as dev_file:
    users = dev_file.readlines()
    dev_favorited_comments, dev_not_favorited_comments  = create_set(users)
    with open('dev_favorite-comments.json','w') as new_json_file:
        json.dump(dev_favorited_comments, new_json_file, indent = 4)
    with open('dev_not_favorite-comments.json','w') as new_json_file:
        json.dump(dev_not_favorited_comments, new_json_file, indent = 4)    