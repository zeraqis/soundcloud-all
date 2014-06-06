#!/usr/bin/env python
import os
import cPickle as pickle
import collections
import csv

sub_dir = '/home/sathya/Dev/soundcloud-data/categorized'
with open('analysis.csv', 'wb') as csv_file:
    for lic_folder in os.listdir(sub_dir):
        print '----------\n----------'
        lic_dir = sub_dir + '/' + str(lic_folder)
        print lic_folder
        print '----------\n----------'
        curr_genres = []
        for genre_folder in os.listdir(lic_dir):
            max_created = "2010/01/01 00:00:00:00"
            min_created = "2014/01/01 00:00:00:00"
            max_comment_count = 0
            number_tracks = 0
            genre_dir = lic_dir + '/' + str(genre_folder)
            curr_genres.append(genre_folder)
            for filename in os.listdir(genre_dir):
                if 'track' in filename:
                    number_tracks += 1
                if 'comment' not in filename:
                    file_dir = genre_dir + '/' + str(filename)
                    with open(file_dir, 'rb') as input:
                        track = pickle.load(input)
                        if max_created < track.created_at:
                            max_created = track.created_at
                        if min_created > track.created_at:
                            min_created = track.created_at
                        if max_comment_count < track.comment_count:
                            max_comment_count = track.comment_count
            row = [genre_folder, lic_folder, max_created, min_created, max_comment_count, number_tracks]
            print row
            writer = csv.writer(csv_file)
            writer.writerow(row)
            comment_count = []
    
    
    