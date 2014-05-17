#!/usr/bin/env python
import os
import cPickle as pickle
import collections
import csv
import math
import itertools

sub_dir = 'D:/Dev/soundcloud data/bulk'
with open('refined.csv', 'wb') as csv_file:
    for lic_folder in os.listdir(sub_dir):
        print '----------\n----------'
        lic_dir = sub_dir + '/' + str(lic_folder)
        print lic_folder
        print '----------\n----------'
        curr_genres = []
        for genre_folder in os.listdir(lic_dir):
            popularity = []
            genre_dir = lic_dir + '/' + str(genre_folder)
            curr_genres.append(genre_folder)
            for filename in os.listdir(genre_dir):
                if 'track' in filename:
                    file_dir = genre_dir + '/' + str(filename)
                    with open(file_dir, 'rb') as input:
                        track = pickle.load(input)
                        if not(track.genre):
                            track_genre = 'None'
                        else:
                            track_genre = track.genre.encode("utf-8")
                        popularity.append([track.license, genre_folder, track_genre, track.favoritings_count*0.6 + track.download_count*0.4
                                           , track.permalink_url, track.id, track.comment_count])
            sorted_popularity = sorted(popularity, key=lambda tup: tup[3])
            writer = csv.writer(csv_file)
            if len(popularity) > 5:
                row = sorted_popularity[1]
                writer.writerow(row)
                row = sorted_popularity[-2]
                writer.writerow(row)
    