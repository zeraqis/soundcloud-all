#!/usr/bin/env python
import json

interactions_favorite = {}
interactions_not_favorite = {}

with open("user-interaction.json", "r") as json_file:
    #big_json = json_file.readlines()
    user_track_dict = json.load(json_file)
    for user in user_track_dict:
        #print user
        if user_track_dict[user]['stats']['comment_and_favorite_count'] > 0:
            if user not in interactions_favorite:
                interactions_favorite[user] = []
            if user not in interactions_not_favorite:
                interactions_not_favorite[user] = []
            #print user_track_dict[user]['stats']['comment_and_favorite_list']
            favorite_list = user_track_dict[user]['stats']['comment_and_favorite_list']
            if len(favorite_list) > 0:
                interactions_favorite[user] = list(favorite_list)
            not_favorite_list = user_track_dict[user]['stats']['comment_and_not_favorite_list']
            if len(not_favorite_list) > 0:
                interactions_not_favorite[user] = list(not_favorite_list)


with open('comment-favorite_user-track.json', 'w') as new_json_file_1:
    json.dump(interactions_favorite, new_json_file_1, indent = 4)

with open('comment-not-favorite_user-track.json', 'w') as new_json_file_2:
    json.dump(interactions_not_favorite, new_json_file_2, indent = 4)