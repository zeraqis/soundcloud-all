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

def feature_extract(dict_model, user, label):
    feat_sets = []
    for comment in list(dict_model[user]['model']):
        if comment!= "" :
            feats = {}
            comment_words = tokenizer(comment)
            for word in comment_words:
                feats[word] = 'token'
            feat_sets.append((feats, label))
    return feat_sets

def tokenizer(comment):
    comment_words = set(wordpunct_tokenize(comment))
    comment_words = comment_words.difference(stop)
    return comment_words

print 'loading train json'
with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_train.json','r') as timed_train_json:
    timed_train_dict = json.load(timed_train_json)

print 'generating model'    
for track in timed_train_dict:
    for user in timed_train_dict[track]:
        if user not in train_model:
            train_model[user] = {}
            train_model[user]['tracks'] = []
            train_model[user]['model'] = []
            train_model[user]['sub_users'] = []
        train_model[user]['tracks'].append(track)
        for sub_user in timed_train_dict[track]:
            train_model[user]['sub_users'].append(sub_user)
            if user != sub_user:
                for time in timed_train_dict[track][sub_user]:
                    train_model[user]['model'].append(timed_train_dict[track][sub_user][time])

print 'loading dev json'
with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_dev.json','r') as timed_dev_json:
    timed_dev_dict = json.load(timed_dev_json)
    
with open('user_metrics.tsv', 'w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter = '\t')
    for user in train_model:
        count_param = len(train_model[user]['model'])
        print 'co-commenters', count_param
        if count_param > 2:
            user_train_feats = {}
            init_size = 0
            print "inside user", user
            print "training user commented"
            user_train_feats = feature_extract(train_model, user, 'commented')
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
                        user_train_feats.extend(feature_extract(train_model, sub_user, 'not-commented'))
            
            print 'classifying'
            classifier = nltk.NaiveBayesClassifier.train(user_train_feats)
            
            dev_feats = []
            dev_set = defaultdict(set)    
            ref_dev_set = defaultdict(set)
            
            print 'generating dev set'
            for track in timed_dev_dict:
                feats = {}
                flag = 0
                for sub_user in timed_dev_dict[track]:
                    if user != sub_user:
                        for time in timed_dev_dict[track][sub_user]:
                            comment = timed_dev_dict[track][sub_user][time]
                            if comment!= "" :
                                comment_words = tokenizer(comment)
                                for word in comment_words:
                                    feats[word] = 'token'
                    else:
                        flag = 1
                if flag == 1:
                    dev_feats.append((feats, 'commented'))
                else:
                    dev_feats.append((feats, 'not-commented'))
            
            print 'classifying dev set'
            for i, (feats,label) in enumerate(dev_feats):
                ref_dev_set[label].add(i)
                observed = classifier.classify(feats)
                dev_set[observed].add(i)
            
            print 'commented_actual', len(ref_dev_set['commented'])
            print 'not-commented_actual', len(ref_dev_set['not-commented'])
            
            print "****USER****", user
            print 'commented precision:', nltk.metrics.precision(ref_dev_set['commented'], dev_set['commented'])
            print 'commented recall:', nltk.metrics.recall(ref_dev_set['commented'], dev_set['commented'])
            print 'commented F-measure:', nltk.metrics.f_measure(ref_dev_set['commented'], dev_set['commented'])
            print 'not-commented precision:', nltk.metrics.precision(ref_dev_set['not-commented'], dev_set['not-commented'])
            print 'not-commented recall:', nltk.metrics.recall(ref_dev_set['not-commented'], dev_set['not-commented'])
            print 'not-commented F-measure:', nltk.metrics.f_measure(ref_dev_set['not-commented'], dev_set['not-commented'])
        
            #classifier.show_most_informative_features(10)
            tsvwriter.writerow([user, count_param, len(user_train_feats), len(ref_dev_set['commented']),  nltk.metrics.precision(ref_dev_set['commented'], dev_set['commented']), nltk.metrics.recall(ref_dev_set['commented'], dev_set['commented']),
                               nltk.metrics.f_measure(ref_dev_set['commented'], dev_set['commented']), len(ref_dev_set['not-commented']), nltk.metrics.precision(ref_dev_set['not-commented'], dev_set['not-commented']),
                               nltk.metrics.recall(ref_dev_set['not-commented'], dev_set['not-commented']), nltk.metrics.f_measure(ref_dev_set['not-commented'], dev_set['not-commented'])])