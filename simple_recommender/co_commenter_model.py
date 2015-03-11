#!/usr/bin/env python
from pandas import DataFrame
import json
import csv
import uuid
import random
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import nltk.data
import sys
import cPickle as pickle

nltk.data.path.append('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nltk_data')

train_model = {}
number_users = 0
stop = stopwords.words('english')

classifier = MultinomialNB()

def tokenizer(comment):
    comment_words = set(wordpunct_tokenize(comment))
    comment_words = comment_words.difference(stop)
    return comment_words

def show_most_informative_features(vectorizer, clf, n=20):
    feat_info = []
    class_labels = clf.classes_
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        feat_info.append("%.4f %-15s %s \t%.4f %-15s %s" % (coef_1, fn_1, class_labels[0], coef_2, fn_2, class_labels[1]))
    return feat_info

print 'loading chunk' + str(sys.argv[1])
with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/simple_recommender/co_commenter_chunks/chunk-' + str(sys.argv[1])) as chunkfile:
    train_model = pickle.load(chunkfile)

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/simple_recommender/train_user_list', 'r') as listfile:
    train_user_set = pickle.load(listfile)

print 'loading dev json'
with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/sampling/timed_dev.json','r') as timed_dev_json:
    timed_dev_dict = json.load(timed_dev_json)
    
for user in train_model:
    print "number_users", number_users
    
    number_users += 1
    init_size = 0
    
    print "inside user", user
    train_feats = []
    
    for comment in list(train_model[user]['model']):
        train_feats.append((comment, 1))
    
    init_size = len(train_feats)
    
    users = train_model.keys()
    random.shuffle(users)
    for sub_user in users:
        if  len(train_feats) >= 2*init_size:
            break
        if list(set(train_model[user]['sub_users']).intersection(set(train_model[sub_user]['sub_users']))) == []:
            if user != sub_user:
                for comment in list(train_model[sub_user]['model']):
                    train_feats.append((comment, 0))
    
    train_df = DataFrame({'text': [], 'class': []})
    
    for comment, label in train_feats:
        train_df = train_df.append(DataFrame({'text': [comment], 'class': [label]}, index=[str(uuid.uuid4())]))
    
    count_vectorizer = CountVectorizer(analyzer = tokenizer)
    
    train_counts = count_vectorizer.fit_transform(numpy.asarray(train_df['text']))
    train_words = train_counts.getnnz()
    train_targets = numpy.asarray(train_df['class'])
    
    classifier.fit(train_counts, train_targets)
    
    with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/simple_recommender/co_commenter_results/'+ user + '_feats.txt','w') as user_feats_file:
        feat_info = show_most_informative_features(count_vectorizer, classifier, n=20)
        for line in feat_info:
            user_feats_file.write(line.encode('utf-8').strip() + '\n')
    
    dev_feats = []
    dev_track_comments = {}
    
    for track in timed_dev_dict:
        feats = {}
        flag = 0
        for sub_user in timed_dev_dict[track]:
            for time in timed_dev_dict[track][sub_user]:
                if sub_user in train_user_set:
                    if track not in dev_track_comments:
                        dev_track_comments[track] = {}
                        dev_track_comments[track]['comments'] = []
                    if user == sub_user:
                        flag = 1
                    else:
                        dev_track_comments[track]['comments'].append(timed_dev_dict[track][sub_user][time])
                    if flag == 1:
                        dev_track_comments[track]['label'] = 1
                    if flag == 0:
                        dev_track_comments[track]['label'] = 0
    
    
    with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/simple_recommender/co_commenter_results/'+ user + '_results.csv', 'w') as user_results_file:
        results_writer = csv.writer(user_results_file)
        results_writer.writerow(['track', 'true_label', 'train_feats', 'dev_feats', 'classifier_accuracy', 'true_nc', 'true_c', 'pred_nc', 'pred_c', 'precision_nc', 'precision_c', 'recall_nc', 'recall_c', 'f_nc', 'f_c', 'avg_prob_nc', 'avg_prob_c'])
        
        for track in dev_track_comments:
            
            if len(dev_track_comments[track]['comments']) >= 1: 
            
                dev_df = DataFrame({'text': [], 'class': []})
                
                for comment in dev_track_comments[track]['comments']:
                    dev_df = dev_df.append(DataFrame({'text': [comment], 'class': [dev_track_comments[track]['label']]}, index=[str(uuid.uuid4())]))
                
                dev_counts = count_vectorizer.transform(numpy.asarray(dev_df['text']))
                dev_words = dev_counts.getnnz()
                
                if dev_words > 0:
                    dev_targets = numpy.asarray(dev_df['class'])
                    
                    pred = classifier.predict(dev_counts)
                    
                    pred_prob = classifier.predict_proba(dev_counts)
                    
                    pred_prob = classifier.predict_proba(dev_counts)
                    
                    avg_prob = []
                    
                    avg_prob.append(numpy.average(numpy.array(pred_prob[:,0])))
                    avg_prob.append(numpy.average(numpy.array(pred_prob[:,1])))
                    
                    precision, recall, f_score, true_support = metrics.precision_recall_fscore_support(dev_targets, pred, labels = [0, 1], average=None)
                    
                    pred_support = [0,0]
                    
                    for pred_label in pred:
                        if pred_label == 0:
                            pred_support[0] += 1
                        if pred_label == 1:
                            pred_support[1] += 1
                    
                    clf_accuracy = metrics.accuracy_score(dev_targets, pred)
                    
                    results_writer.writerow([track, dev_track_comments[track]['label'], train_words, dev_words, clf_accuracy, true_support[0], true_support[1], pred_support[0], pred_support[1], precision[0], precision[1], recall[0], recall[1], f_score[0], f_score[1], avg_prob[0], avg_prob[1]])