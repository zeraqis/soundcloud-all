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

s = """<?xml version="1.0" encoding = "utf-8"?>"""
sub_dir1 = '/home/sathya/Dev/soundcloud-data/categorized'
sub_dir2 = '/home/sathya/Dev/soundcloud-data/pickle'
with open('drop_tracks.txt', 'rb') as txt:
    for line in txt:
        line = line.strip() + '.track'
        for root1, dirs, files in os.walk(sub_dir1):
                for filename in files:
                    if line in filename:
                        track_dir = os.path.join(root1, filename)
                        with open(track_dir, 'rb') as track_input:
                            track = pickle.load(track_input)
                        file_index = int(math.ceil(track.comment_count/200))
                        id_ = track.id
                        tmp = os.path.relpath(root1,sub_dir1)
                        license_, genre = tmp.split('/')
                        root2 = sub_dir2 + '/' + license_ + '/' + genre
                        if not os.path.exists(root2):
                            os.makedirs(root2)
                        if file_index == 0:
                                file_index = 1
                        for i in range(file_index):
                            comment_filename = str(id_) + '_' + str(i+1) +'.comment'
                            comment_dir = os.path.join(root1, comment_filename)
                            with open(comment_dir, 'rb') as comment_in:
                                comments = pickle.load(comment_in)
                                comment_count = 0
                                for comment in reversed(comments):
                                    if comment.timestamp:
                                        try:
                                            comment.body.decode('ascii')
                                        except UnicodeEncodeError:
                                            a = 1
                                        else:
                                            if len(comment.body) > 1 and 'http' not in comment.body and comment.user_id != track.user_id:
                                                comment_count += 1