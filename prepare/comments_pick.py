#!/usr/bin/env python
import cPickle as pickle
import math
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml_pretty import prettify
from preproc.filter import remove_diacritic, check_exist
import nltk
import re
import lxml.etree as et
import StringIO
from xml.etree.ElementTree import XML
import os

sub_dir1 = '/home/sathya/Dev/soundcloud-data/xml_original'
fd = nltk.FreqDist()
terms = []
comment_ids = []
count = 0
with open('terms.txt', 'rb') as txt:
    for line in txt:
        terms.append(line.strip())
    
for root1, dirs, files in os.walk(sub_dir1):
    for filename in files:
        track_dir = os.path.join(root1, filename)
        with open(track_dir, 'rb') as xmlfile:
            reader = xmlfile.read()
            e = XML(reader)
            #track = e.find('track')
            #print(track.get('created_at'))
            comments = e.findall('comment')
            for comment in comments:
                body = comment.get('body')
                comment_id = comment.get('comment_id')
                words = nltk.regexp_tokenize(body, pattern=r'\w+|[^\w\s]+')
                for word in words:
                    if comment_id not in comment_ids:
                        if word in terms and comment_id not in comment_ids:
                            #print body
                            comment_ids.append(comment_id)
for comment_id in comment_ids:
    print comment_id

with open('comment_ids.txt', 'wb') as txt:
    for comment_id in comment_ids:
        txt.write(str(comment_id) +'\n')
    