#!/usr/bin/env python
import nltk
nltk.data.path.append("/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nltk_data")
import nltk.classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import json
from collections import defaultdict
import csv
import random

stop = stopwords.words('english')
train_model = {}
dev_user_list = []
train_user_list = []
number_users = 0


print 'loading train json'
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

train_user_set = set(train_user_list)

print 'train model len', len(train_model)

print 'loading dev json'
with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_dev.json','r') as timed_dev_json:
    timed_dev_dict = json.load(timed_dev_json)
    
with open('user_metrics_baseline_past.tsv', 'w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter = '\t')
    
    for user in train_model:
        print "number_users", number_users
        if number_users > 100:
            break
        number_users += 1
        init_size = 0
        print "inside user", user
        
        dev_set = defaultdict(set)    
        ref_dev_set = defaultdict(set)
        
        print 'classifying dev set'
        for i, track in enumerate(timed_dev_dict):
            if list(set(timed_dev_dict[track]).intersection(train_user_set)) != []:
                if user in set(timed_dev_dict[track]):
                    label = 'commented'
                else:
                    label = 'not-commented'
                ref_dev_set[label].add(i)
                if track in set(train_model[user]['tracks']):
                    observed = 'commented'
                else:
                    observed = 'not-commented'
                dev_set[observed].add(i)
        
        print 'commented_actual', len(ref_dev_set['commented'])
        print 'commented predicted', len(dev_set['commented'])
        print 'not-commented_actual', len(ref_dev_set['not-commented'])
        print 'not-commented predicted', len(dev_set['not-commented'])
        
        print "****USER****", user
        print 'commented precision:', nltk.metrics.precision(ref_dev_set['commented'], dev_set['commented'])
        print 'commented recall:', nltk.metrics.recall(ref_dev_set['commented'], dev_set['commented'])
        print 'commented F-measure:', nltk.metrics.f_measure(ref_dev_set['commented'], dev_set['commented'])
        print 'not-commented precision:', nltk.metrics.precision(ref_dev_set['not-commented'], dev_set['not-commented'])
        print 'not-commented recall:', nltk.metrics.recall(ref_dev_set['not-commented'], dev_set['not-commented'])
        print 'not-commented F-measure:', nltk.metrics.f_measure(ref_dev_set['not-commented'], dev_set['not-commented'])
    
        
        tsvwriter.writerow([user, len(ref_dev_set['commented']), len(dev_set['commented']), nltk.metrics.precision(ref_dev_set['commented'], dev_set['commented']), nltk.metrics.recall(ref_dev_set['commented'], dev_set['commented']),
                           nltk.metrics.f_measure(ref_dev_set['commented'], dev_set['commented']), len(ref_dev_set['not-commented']), len(dev_set['not-commented']), nltk.metrics.precision(ref_dev_set['not-commented'], dev_set['not-commented']),
                           nltk.metrics.recall(ref_dev_set['not-commented'], dev_set['not-commented']), nltk.metrics.f_measure(ref_dev_set['not-commented'], dev_set['not-commented'])])