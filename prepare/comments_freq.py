#!/usr/bin/env python
import os
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

sub_dir1 = '/home/sathya/Dev/soundcloud-data/xml_original'
fd = nltk.FreqDist()

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
                            if 'piano' in body:
                                words = nltk.regexp_tokenize(body, pattern=r'\w+|[^\w\s]+')
                                for word in words:
                                    if 'piano' in word:
                                        fd.inc(word)
freq_tuples = fd.items()
with open('piano.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '=')
    for item in freq_tuples:
        writer.writerow(item)