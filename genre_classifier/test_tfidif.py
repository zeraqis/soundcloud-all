#!/usr/bin/env python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from pandas import DataFrame
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import nltk
import itertools
import scipy.sparse
import numpy

nltk.data.path.append('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/nltk_data')

def tokenizer(comment):
    stop = stopwords.words('english')
    comment_words = wordpunct_tokenize(comment)
    filtered_words = [w for w in comment_words if not w in stop]
    return filtered_words

custom_count_vectorizer = TfidfVectorizer(analyzer = tokenizer, min_df = 2)
#custom_count_vectorizer = CountVectorizer(analyzer = tokenizer)

df = DataFrame({'text': [], 'class': []})
df = df.append(DataFrame({'text': [ "I like it!!!!"], 'class': ['tmp']}, index=[1]))
df = df.append(DataFrame({'text': [ "I don't like it!!!!!!!!!"], 'class': ['tmp']}, index=[2]))

#print df

custom_counts = custom_count_vectorizer.fit_transform(numpy.asarray(df['text']))

print custom_count_vectorizer.get_feature_names()
print custom_counts.todense()

dense_custom_counts = custom_counts.todense()[1].tolist()[0]
phrase_scores = [pair for pair in zip(range(0, len(dense_custom_counts)), dense_custom_counts)]
phrase_scores = sorted(phrase_scores, key=lambda t: t[1], reverse=True)
for i, score in phrase_scores:
    print score, custom_count_vectorizer.get_feature_names()[i]