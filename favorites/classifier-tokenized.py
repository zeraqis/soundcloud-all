#!/usr/bin/env python
import nltk.classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import wordpunct_tokenize
#from nltk.corpus import stopwords
import json
from collections import defaultdict

train_feats = []
test_feats = []
dev_feats = []
test_set = defaultdict(set)
dev_set = defaultdict(set)    
ref_test_set = defaultdict(set)
ref_dev_set = defaultdict(set)

def feature_extract(json_set, label):
    feat_sets = []
    for user in json_set:
        for track in json_set[user]:
            for comment in list(json_set[user][track]):
                if comment!= "" :
                    feats = {}
                    comment_words = tokenizer(comment)
                    for word in comment_words:
                        feats[word] = 'token'
                    feat_sets.append((feats, label))
    return feat_sets

def tokenizer(comment):
    comment_words = set(wordpunct_tokenize(comment))
    comment_words = comment_words.difference(stopwords)
    return comment_words

with open('english', 'r') as stopfile:
    stopwords = list(stopfile.read().splitlines())

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

train_feats = feature_extract(train_favorite_comments_json, 'favorite')
train_feats.extend(feature_extract(train_not_favorite_comments_json, 'not-favorite'))
test_feats = feature_extract(test_favorite_comments_json, 'favorite')
test_feats.extend(feature_extract(test_not_favorite_comments_json, 'not-favorite'))
dev_feats = feature_extract(dev_favorite_comments_json, 'favorite')
dev_feats.extend(feature_extract(dev_not_favorite_comments_json, 'not-favorite'))

classifier = nltk.NaiveBayesClassifier.train(train_feats)

for i, (feats,label) in enumerate(test_feats):
    ref_test_set[label].add(i)
    observed = classifier.classify(feats)
    test_set[observed].add(i)

for i, (feats,label) in enumerate(dev_feats):
    ref_dev_set[label].add(i)
    observed = classifier.classify(feats)
    dev_set[observed].add(i)

#print "******TEST SET******"
#print 'favorite precision:', nltk.metrics.precision(ref_test_set['favorite'], test_set['favorite'])
#print 'favorite recall:', nltk.metrics.recall(ref_test_set['favorite'], test_set['favorite'])
#print 'favorite F-measure:', nltk.metrics.f_measure(ref_test_set['favorite'], test_set['favorite'])
#print 'not-favorite precision:', nltk.metrics.precision(ref_test_set['not-favorite'], test_set['not-favorite'])
#print 'not-favorite recall:', nltk.metrics.recall(ref_test_set['not-favorite'], test_set['not-favorite'])
#print 'not-favorite F-measure:', nltk.metrics.f_measure(ref_test_set['not-favorite'], test_set['not-favorite'])

print "******DEV SET******"
print 'favorite precision:', nltk.metrics.precision(ref_dev_set['favorite'], dev_set['favorite'])
print 'favorite recall:', nltk.metrics.recall(ref_dev_set['favorite'], dev_set['favorite'])
print 'favorite F-measure:', nltk.metrics.f_measure(ref_dev_set['favorite'], dev_set['favorite'])
print 'not-favorite precision:', nltk.metrics.precision(ref_dev_set['not-favorite'], dev_set['not-favorite'])
print 'not-favorite recall:', nltk.metrics.recall(ref_dev_set['not-favorite'], dev_set['not-favorite'])
print 'not-favorite F-measure:', nltk.metrics.f_measure(ref_dev_set['not-favorite'], dev_set['not-favorite'])
    
classifier.show_most_informative_features(10)