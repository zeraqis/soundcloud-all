#!/usr/bin/env python
from sklearn.feature_extraction.text import CountVectorizer
from pandas import DataFrame
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import nltk
import itertools
import scipy.sparse

nltk.data.path.append('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nltk_data')

def tokenizer(comment):
    stop = stopwords.words('english')
    comment_words = wordpunct_tokenize(comment)
    filtered_words = [w for w in comment_words if not w in stop]
    return filtered_words


custom_count_vectorizer = CountVectorizer(analyzer = tokenizer)

df = DataFrame({'text': [ "I like it!!!!"], 'class': ['tmp']})

custom_counts = custom_count_vectorizer.fit_transform(df['text'])

print custom_counts
print custom_counts.getnnz()
print custom_count_vectorizer.get_feature_names()

coo_custom_counts = custom_counts.tocoo()

for i,j,v in itertools.izip(coo_custom_counts.row, coo_custom_counts.col, coo_custom_counts.data):
    print custom_count_vectorizer.get_feature_names()[j], v

dev_df = DataFrame({'text': [ "sdijkfhskdjfn lkfgjhldkfgj fjkghdkfjhg dkfljghfdkljhg dflikghxfljgh"], 'class': ['tmp']})

dev_custom_counts = custom_count_vectorizer.transform(dev_df['text'])

print dev_custom_counts
print dev_custom_counts.getnnz()
print custom_count_vectorizer.get_feature_names()

coo_dev_custom_counts = dev_custom_counts.tocoo()

for i,j,v in itertools.izip(coo_dev_custom_counts.row, coo_dev_custom_counts.col, coo_dev_custom_counts.data):
    print custom_count_vectorizer.get_feature_names()[j], v