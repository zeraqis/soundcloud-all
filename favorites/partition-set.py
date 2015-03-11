#!/usr/bin/env python

import json
import random

def chunks(lst,n):
    return [ lst[i::n] for i in xrange(n) ]

with open('comment-favorite_user-track.json', 'r') as json_file:
    interactions = json.load(json_file)
    users = list(interactions.keys())
    random.shuffle(users)
    users_lol = chunks(users, 5)
    #print users_lol[0]
    train_users = users_lol[0] + users_lol[1] + users_lol[2]
    print len(train_users)
    dev_users = users_lol[3]
    print len(dev_users)
    test_users = users_lol[4]
    print len(test_users)
    
    with open('train_users.txt', 'w') as train_txt_file:
        for user in train_users:
            train_txt_file.write(user)
            train_txt_file.write('\n')
    
    with open('dev_users.txt', 'w') as dev_txt_file:
        for user in dev_users:
            dev_txt_file.write(user)
            dev_txt_file.write('\n')

    with open('test_users.txt', 'w') as test_txt_file:
        for user in test_users:
            test_txt_file.write(user)
            test_txt_file.write('\n')