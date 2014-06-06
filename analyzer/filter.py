#!/usr/bin/env python
import os
import cPickle as pickle
import math

sub_dir = '/home/sathya/Dev/soundcloud-data/uncategorized'
track_paths = []
comment_paths = []
count = 0
for root, dirs, files in os.walk(sub_dir):
    for filename in files:
        if 'track' in filename:
            file_dir = os.path.join(root, filename)
            with open(file_dir, 'rb') as input:
                curr_comment = 0
                track = pickle.load(input)
                file_index = int(math.ceil(track.comment_count/200))
                if file_index == 0:
                    file_index = 1
                #print file_index
                for i in range(file_index):
                    comment_filename = str(track.id) + '_' + str(i+1) +'.comment'
                    comment_dir = os.path.join(root, comment_filename)
                    #print comment_dir
                    try:
                        with open(comment_dir, 'rb') as comment_in:
                            comments = pickle.load(comment_in)
                            for comment in comments:
                                if comment.timestamp and track.user_id != comment.user_id and track.streamable:
                                    curr_comment += 1
                    except IOError as e:
                        print file_dir
                        track_paths.append(file_dir)
                if curr_comment < 4:
                    track_paths.append(file_dir)
                    for i in range(file_index):
                        comment_filename = str(track.id) + '_' + str(i+1) +'.comment'
                        comment_dir = os.path.join(root, comment_filename)
                        if comment_dir:
                            comment_paths.append(comment_dir)


for dirs in track_paths:
    try:
        os.remove(dirs)
    except:
        print "Done"

for dires in comment_paths:
    try:
        os.remove(dirs)
    except:
        print "No Comment"