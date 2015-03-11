#!/usr/bin/env python
import json

train_model = {}
dev_lm_dict = {}
dev_user_list = []
train_user_list = []

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/dev_users.tsv', 'r') as dev_tsvfile:
    dev_user_list = [x.strip() for x in dev_tsvfile.readlines()]

dev_user_set = set(dev_user_list)

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_train.json','r') as timed_train_json:
    timed_train_dict = json.load(timed_train_json)
    
for track in timed_train_dict:
    for user in timed_train_dict[track]:
        if user in dev_user_set:
            if user not in train_model:
                train_user_list.append(user)
                train_model[user] = {}
                train_model[user]['tracks'] = []
                train_model[user]['model'] = []
                train_model[user]['sub_users'] = []
            train_model[user]['tracks'].append(track)
            for sub_user in timed_train_dict[track]:
                train_model[user]['sub_users'].append(sub_user)
                if user == sub_user:
                    for time in timed_train_dict[track][sub_user]:
                        train_model[user]['model'].append(timed_train_dict[track][sub_user][time])

with open('model_train.json', 'w') as model_train_json:
    json.dump(train_model, model_train_json, indent = 4)