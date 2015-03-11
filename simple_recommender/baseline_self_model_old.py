#!/usr/bin/env python
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

def feature_extract(comment_list, label):
    feat_sets = []
    all_words = []
    feats = {}
    for comment in comment_list:
        if comment!= "" :
            feats = {}
            comment_words = tokenizer(comment)
            curr_words = nltk.FreqDist(w.lower() for w in comment_words)
            for word in curr_words.keys():
                feats[word] = True
        feat_sets.append((feats, label))
    return feat_sets

def tokenizer(comment):
    comment_words = set(wordpunct_tokenize(comment))
    comment_words = comment_words.difference(stop)
    return comment_words

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
    
with open('user_metrics_baseline_self.tsv', 'w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter = '\t')
    
    for user in train_model:
        print "number_users", number_users
        if number_users > 5:
            break
        number_users += 1
        user_train_feats = {}
        init_size = 0
        print "inside user", user
        
        print "training user commented"
        user_train_feats = feature_extract(list(train_model[user]['model']), 'commented')
        init_size = len(user_train_feats)
        
        print "training user not-commented"
        users = train_model.keys()
        random.shuffle(users)
        for sub_user in users:
            if  len(user_train_feats) >= 2*init_size:
                break
            if list(set(train_model[user]['sub_users']).intersection(set(train_model[sub_user]['sub_users']))) == []:
                print "inside sub-user", sub_user
                if user != sub_user:
                    user_train_feats.extend(feature_extract(list(train_model[sub_user]['model']), 'not-commented'))
        
        print 'train feats len', len(user_train_feats)
        
        print 'classifying'
        classifier = nltk.NaiveBayesClassifier.train(user_train_feats)
        
        dev_feats = []
        dev_set = defaultdict(set)    
        ref_dev_set = defaultdict(set)
        dev_track_comments = {}
        
        print 'generating dev set'
        for track in timed_dev_dict:
            feats = {}
            flag = 0
            for sub_user in timed_dev_dict[track]:
                if sub_user in train_user_set:
                    if track not in dev_track_comments:
                        dev_track_comments[track] = {}
                        dev_track_comments[track]['comments'] = []
                    if user == sub_user:
                        flag = 1
                    else:
                        dev_track_comments[track]['comments'].extend(list(timed_dev_dict[track][sub_user]))
                    if flag == 1:
                        dev_track_comments[track]['label'] = 'commented'
                    if flag == 0:
                        dev_track_comments[track]['label'] = 'not-commented'
        
        for track in dev_track_comments:
            dev_feats.extend(feature_extract(list(dev_track_comments[track]['comments']), dev_track_comments[track]['label']))
        
        print 'dev feats len', len(dev_feats)
        
        print 'classifying dev set'
        for i, (feats,label) in enumerate(dev_feats):
            ref_dev_set[label].add(i)
            observed = classifier.classify(feats)
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
    
        classifier.show_most_informative_features(10)
        
        tsvwriter.writerow([user, len(user_train_feats), len(dev_feats), len(ref_dev_set['commented']), len(dev_set['commented']), nltk.metrics.precision(ref_dev_set['commented'], dev_set['commented']), nltk.metrics.recall(ref_dev_set['commented'], dev_set['commented']),
                           nltk.metrics.f_measure(ref_dev_set['commented'], dev_set['commented']), len(ref_dev_set['not-commented']), len(dev_set['not-commented']), nltk.metrics.precision(ref_dev_set['not-commented'], dev_set['not-commented']),
                           nltk.metrics.recall(ref_dev_set['not-commented'], dev_set['not-commented']), nltk.metrics.f_measure(ref_dev_set['not-commented'], dev_set['not-commented']), classifier.most_informative_features(10)])