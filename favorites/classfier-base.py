#!/usr/bin/env python
import nltk
import json
import random
import collections

train_feats = []
test_feats = []
dev_feats = []
test_set = collections.defaultdict(set)
dev_set = collections.defaultdict(set)    
ref_test_set = collections.defaultdict(set)
ref_dev_set = collections.defaultdict(set)

with open('train_favorite-comments.json','r') as json_file:
    train_favorite_comments_json = json.load(json_file)
    
with open('train_not_favorite-comments.json','r') as json_file:
    train_not_favorite_comments_json = json.load(json_file)

with open('test_favorite-comments.json','r') as json_file:
    test_favorite_comments_json = json.load(json_file)

with open('test_not_favorite-comments.json','r') as json_file:
    test_not_favorite_comments_json = json.load(json_file)

with open('dev_favorite-comments.json','r') as json_file:
    dev_favorite_comments_json = json.load(json_file)

with open('dev_not_favorite-comments.json','r') as json_file:
    dev_not_favorite_comments_json = json.load(json_file)

for user in train_favorite_comments_json:
    for track in train_favorite_comments_json[user]:
        for comment in list(train_favorite_comments_json[user][track]):
            if comment!= "":
                train_feats.append(({'comment':comment}, 'favorite'))

for user in train_not_favorite_comments_json:
    for track in train_not_favorite_comments_json[user]:
        for comment in list(train_not_favorite_comments_json[user][track]):
            if comment!= "":
                train_feats.append(({'comment':comment}, 'not-favorite'))

#random.shuffle(train_feats)

for user in test_favorite_comments_json:
    for track in test_favorite_comments_json[user]:
        for comment in list(test_favorite_comments_json[user][track]):
            if comment!= "":
                test_feats.append(({'comment':comment}, 'favorite'))

for user in test_not_favorite_comments_json:
    for track in test_not_favorite_comments_json[user]:
        for comment in list(test_not_favorite_comments_json[user][track]):
            if comment!= "":
                test_feats.append(({'comment':comment}, 'not-favorite'))

for user in dev_favorite_comments_json:
    for track in dev_favorite_comments_json[user]:
        for comment in list(dev_favorite_comments_json[user][track]):
            if comment!= "":
                dev_feats.append(({'comment':comment}, 'favorite'))

for user in dev_not_favorite_comments_json:
    for track in dev_not_favorite_comments_json[user]:
        for comment in list(dev_not_favorite_comments_json[user][track]):
            if comment!= "":
                dev_feats.append(({'comment':comment}, 'not-favorite'))


classifier = nltk.NaiveBayesClassifier.train(train_feats)

for i, (feats,label) in enumerate(test_feats):
    ref_test_set[label].add(i)
    observed = classifier.classify(feats)
    test_set[observed].add(i)

for i, (feats,label) in enumerate(dev_feats):
    ref_dev_set[label].add(i)
    observed = classifier.classify(feats)
    dev_set[observed].add(i)

print "******TEST SET******"
print 'favorite precision:', nltk.metrics.precision(ref_test_set['favorite'], test_set['favorite'])
print 'favorite recall:', nltk.metrics.recall(ref_test_set['favorite'], test_set['favorite'])
print 'favorite F-measure:', nltk.metrics.f_measure(ref_test_set['favorite'], test_set['favorite'])
print 'not-favorite precision:', nltk.metrics.precision(ref_test_set['not-favorite'], test_set['not-favorite'])
print 'not-favorite recall:', nltk.metrics.recall(ref_test_set['not-favorite'], test_set['not-favorite'])
print 'not-favorite F-measure:', nltk.metrics.f_measure(ref_test_set['not-favorite'], test_set['not-favorite'])

print "******DEV SET******"
print 'favorite precision:', nltk.metrics.precision(ref_dev_set['favorite'], dev_set['favorite'])
print 'favorite recall:', nltk.metrics.recall(ref_dev_set['favorite'], dev_set['favorite'])
print 'favorite F-measure:', nltk.metrics.f_measure(ref_dev_set['favorite'], dev_set['favorite'])
print 'not-favorite precision:', nltk.metrics.precision(ref_dev_set['not-favorite'], dev_set['not-favorite'])
print 'not-favorite recall:', nltk.metrics.recall(ref_dev_set['not-favorite'], dev_set['not-favorite'])
print 'not-favorite F-measure:', nltk.metrics.f_measure(ref_dev_set['not-favorite'], dev_set['not-favorite'])
    
classifier.show_most_informative_features(50)