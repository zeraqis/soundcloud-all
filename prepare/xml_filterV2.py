#!/usr/bin/env python
import os
import cPickle as pickle
import math
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml_pretty import prettify
import gnosis.xml.pickle

sub_dir1 = '/home/sathya/Dev/soundcloud-data/categorized'
sub_dir2 = '/home/sathya/Dev/soundcloud-data/categorized_comments'
with open('relative_week.csv', 'rb') as track_file:
    reader = csv.reader(track_file)
    for row in reader:
        id_ = row[0]
        license = row[2]
        genre = row[3]
        root1 = sub_dir1 + '/' + license + '/' + genre
        root2 = sub_dir2 + '/' + license + '/' + genre
        if not os.path.exists(root2):
            os.makedirs(root2)
        xml_filename = id_ + '.xml'
        xml_dir = os.path.join(root2, xml_filename)
        track_filename = id_ + '.track'
        track_dir = os.path.join(root1, track_filename)
        with open(track_dir, 'rb') as track_input:
            track = pickle.load(track_input)
        file_index = int(math.ceil(track.comment_count/200))
        with open(xml_dir, 'wb') as xml_file:
            
            if file_index == 0:
                file_index = 1
            for i in range(file_index):
                comment_filename = str(id_) + '_' + str(i+1) +'.comment'
                comment_dir = os.path.join(root1, comment_filename)
                with open(comment_dir, 'rb') as comment_in:
                    comments = pickle.load(comment_in)
                    for comment in reversed(comments):
                        if comment.timestamp:
                            try:
                                comment.body.decode('ascii')
                            except UnicodeEncodeError:
                                a = 1
                            else:
                                if len(comment.body) > 1 and 'http' not in comment.body and comment.user_id != track.user_id:
                                    
            #print prettify(sound)
            
            tree.write(xml_file)
            break