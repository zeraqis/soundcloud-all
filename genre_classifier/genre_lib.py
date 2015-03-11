#!/usr/bin/env python
import cPickle as pickle
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn import metrics
from sklearn import linear_model
import json
from pandas import DataFrame
import numpy
import csv
import itertools
import operator

def tokenizer(comment):
    stop = stopwords.words('english')
    comment_words = wordpunct_tokenize(comment)
    filtered_words = [w for w in comment_words if not w in stop]
    return filtered_words

def show_most_informative_features(clf, vectorizer, tsvwriter, n=50):
    feat_info = {}
    class_labels = clf.classes_
    feature_names = vectorizer.get_feature_names()
    for i, class_label in enumerate(class_labels):
        top_indices = numpy.argsort(clf.coef_[i])[-n:]
        top_coef = numpy.sort(clf.coef_[i])[-n:]
        top = zip(top_coef, top_indices)
        #print("%s: %s" % (class_label, " ".join(feature_names[j] for j in top20_indices))).encode('utf-8')
        for prob, index in top:
            tsvwriter.writerow([class_label, feature_names[index].encode('utf-8'), prob])

def gen_model(genre_dict, sample):
    genre_model = {}
    for track in genre_dict:
        track_genre = genre_dict[track]['genre']
        for user in genre_dict[track]:
            if user != 'genre':
                for time in genre_dict[track][user]:
                    if sample == 'chunk':
                        if track_genre not in genre_model:
                            genre_model[track_genre] = []
                        genre_model[track_genre].append(genre_dict[track][user][time])
                    if sample == 'track':
                        if track_genre not in genre_model:
                            genre_model[track_genre] = {}
                        if track not in genre_model[track_genre]:
                            genre_model[track_genre][track] = []
                        genre_model[track_genre][track].append(genre_dict[track][user][time])
                    if sample == 'user':
                        if track_genre not in genre_model:
                            genre_model[track_genre] = {}
                        if track not in genre_model[track_genre]:
                            genre_model[track_genre][user] = []
                        genre_model[track_genre][user].append(genre_dict[track][user][time])
    if sample == 'chunk':
        for genre in genre_model:
            genre_model[genre] = " ".join(genre_model[genre])
    if sample == 'track':
        for genre in genre_model:
            for track in genre_model[genre]:
                genre_model[genre][track] = " ".join(genre_model[genre][track])
    if sample == 'user':
        for genre in genre_model:
            for user in genre_model[genre]:
                genre_model[genre][user] = " ".join(genre_model[genre][user])
    return genre_model

def frequent_words(genre_model, label):
    for genre in genre_model:
        with open(label + '_' + genre + '.counts', 'w') as countsfile:
            tsvwriter = csv.writer(countsfile, delimiter='\t')
            fdist = nltk.FreqDist(tokenizer(genre_model[genre]))
            for k,v in fdist.most_common(50):
                tsvwriter.writerow([k.encode('utf-8'), v])

def classify_this(train_df, dev_df, clf, vectorizer, name, selection_flag):
    
    print 'classifying ' + name
    
    train_vector = vectorizer.fit_transform(numpy.asarray(train_df['text']))
    train_labels = numpy.asarray(train_df['class'])
    
    dev_vector = vectorizer.transform(numpy.asarray(dev_df['text']))
    dev_labels = numpy.asarray(dev_df['class'])
    
    if selection_flag:
        ch2 = SelectKBest(chi2, k=selection_flag)
        train_vector = ch2.fit_transform(train_vector, train_labels)
        dev_vector = ch2.transform(dev_vector)
    
    clf.fit(train_vector, train_labels)
    pred_labels = clf.predict(dev_vector)

    labels_tuple = zip(pred_labels, dev_labels)
    
    if 'nb' in name:
        pred_labels_prob = clf.predict_proba(dev_vector)
    
    clf_accuracy = metrics.accuracy_score(dev_labels, pred_labels)
    
    with open(name + '.feats', 'w') as feats_file:
        tsvwriter = csv.writer(feats_file, delimiter='\t')
        show_most_informative_features(clf, vectorizer, tsvwriter)
    
    precision, recall, f_score, true_support = metrics.precision_recall_fscore_support(dev_labels, pred_labels, labels=clf.classes_, average='weighted')
    
    with open(name + '.results', 'w') as results_file:
        tsvwriter = csv.writer(results_file, delimiter='\t')
        tsvwriter.writerow(['precision','recall','f_score'])
        tsvwriter.writerow([precision, recall, f_score])
    
    precision, recall, f_score, true_support = metrics.precision_recall_fscore_support(dev_labels, pred_labels, labels=clf.classes_, average=None)
    
    with open(name + '_label.results', 'w') as results_file:
        tsvwriter = csv.writer(results_file, delimiter='\t')
        tsvwriter.writerow(['label', 'precision','recall','f_score', 'true_support'])
        for i, label in enumerate(clf.classes_):
            tsvwriter.writerow([label, precision[i], recall[i], f_score[i], true_support[i]])