#!/usr/bin/env python
from xml.etree.ElementTree import XML
import os
import nltk
import csv

sub_dir = '/home/sathya/Dev/soundcloud-data/xml_original_final'
with open('hit_input.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            file_dir = os.path.join(root, filename)
            with open(file_dir, 'rb') as xmlfile:
                reader = xmlfile.read()
                e = XML(reader)
                track = e.find('track')
                id_ = track.get('track_id')
                uri = track.get('uri')
                comments = e.findall('comment')
                for comment in comments:
                    body = comment.get('body')
                    terms = []
                    with open('terms.txt', 'rb') as txtfile:
                        for line in txtfile:
                            for word in nltk.regexp_tokenize(body, pattern=r'\.|(\s+)', gaps = True):
                                if line.strip() == word:
                                    terms.append(word)
                                    #print body, "lah", word
                    timestamp = comment.get('timestamp')
                    for term in terms:
                        row = [id_,uri,body,term,timestamp]
                        csvwriter.writerow(row)