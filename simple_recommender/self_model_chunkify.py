#!/usr/bin/env python
import json
import csv
import cPickle as pickle
from random import shuffle

train_model = {}
dev_user_list = []
train_user_list = []

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_train.json','r') as timed_train_json:
    timed_train_dict = json.load(timed_train_json)

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/dev_users.tsv', 'r') as dev_tsvfile:
    dev_user_list = [x.strip() for x in dev_tsvfile.readlines()]

dev_user_set = set(dev_user_list)

print 'generating train model'    
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

shuffle(train_user_list)

train_user_set = set(train_user_list)

with open('train_user_list', 'w') as listfile:
    pickle.dump(train_user_set, listfile)

train_chunks = chunks(train_user_list, 500)

for i, chunk in enumerate(train_chunks):
    chunk_dict = {}
    for user in chunk:
        chunk_dict[user] = {}
        chunk_dict[user]['tracks'] = []
        chunk_dict[user]['model'] = []
        chunk_dict[user]['sub_users'] = []
        chunk_dict[user]['tracks'] = list(train_model[user]['tracks'])
        chunk_dict[user]['model'] = list(train_model[user]['model'])
        chunk_dict[user]['sub_users'] = list(train_model[user]['sub_users'])
    with open('self_chunks/chunk-'+ str(i), 'w') as chunkfile:
        pickle.dump(chunk_dict, chunkfile)