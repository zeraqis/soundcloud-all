#!/usr/bin/env python
import os
import cPickle as pickle
import math

sub_dir = 'D:/Dev/soundcloud data/bulk'
track_paths = []
count = 0
for root, dirs, files in os.walk(sub_dir):
    for filename in files:
        if '100422101' in filename:
            file_dir = os.path.join(root, filename)
            with open(file_dir, 'rb') as input:
                track = pickle.load(input)
                print track.comment_count