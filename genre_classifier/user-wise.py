#!/usr/bin/env python
import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn import linear_model
from pandas import DataFrame
from nltk import data
from genre_lib import classify_this, gen_model, tokenizer, frequent_words
import json

data.path.append('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nltk_data')

print 'loading train'
with open('genre_train_dict.pickle', 'r') as genre_train_file:
    genre_train_dict = pickle.load(genre_train_file)
genre_train_model = gen_model(genre_train_dict, 'chunk')

print 'loading dev'
with open('genre_dev_dict.pickle', 'r') as genre_dev_file:
    genre_dev_dict = pickle.load(genre_dev_file)
genre_dev_model = gen_model(genre_dev_dict, 'user')

#print 'computing freq dist'

#frequent_words(genre_train_model, 'train')
#frequent_words(genre_dev_model, 'dev')

train_df = DataFrame({'text': [], 'class': []})
dev_df = DataFrame({'text': [], 'class': []})

for genre in genre_train_model:
    train_df = train_df.append(DataFrame({'text': [genre_train_model[genre]], 'class': [genre]}))

for genre in genre_dev_model:
    for user in genre_dev_model[genre]:
        dev_df = dev_df.append(DataFrame({'text': [genre_dev_model[genre][user]], 'class': [genre]}))

count_vectorizer = CountVectorizer(analyzer = tokenizer)
tfidf_vectorizer = TfidfVectorizer(analyzer = tokenizer)

nb_classifier = MultinomialNB()
svc_classifier = LinearSVC()
svc_sq_classifier = LinearSVC(loss='l2')

classify_this(train_df, dev_df, nb_classifier, count_vectorizer, 'user_count_nb', 0)
classify_this(train_df, dev_df, svc_classifier, count_vectorizer, 'user_count_svc', 0)
classify_this(train_df, dev_df, svc_sq_classifier, count_vectorizer, 'user_count_svc_sq', 0)

classify_this(train_df, dev_df, nb_classifier, tfidf_vectorizer, 'user_tfidf_nb', 0)
classify_this(train_df, dev_df, svc_classifier, tfidf_vectorizer, 'user_tfidf_svc', 0)
classify_this(train_df, dev_df, svc_sq_classifier, tfidf_vectorizer, 'user_tfidf_svc_sq', 0)

classify_this(train_df, dev_df, nb_classifier, count_vectorizer, 'user_count_select_nb', 1000)
classify_this(train_df, dev_df, svc_classifier, count_vectorizer, 'user_count_select_svc', 1000)
classify_this(train_df, dev_df, svc_sq_classifier, count_vectorizer, 'user_count_select_svc_sq', 1000)

classify_this(train_df, dev_df, nb_classifier, tfidf_vectorizer, 'user_tfidf_select_nb', 1000)
classify_this(train_df, dev_df, svc_classifier, tfidf_vectorizer, 'user_tfidf_select_svc', 1000)
classify_this(train_df, dev_df, svc_sq_classifier, tfidf_vectorizer, 'user_tfidf_select_svc_sq', 1000)