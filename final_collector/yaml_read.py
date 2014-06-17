#!/usr/bin/env python
import yaml
import os

sub_dir = '/home/sathya/Dev/soundcloud-data/bulk_pickle'
with open('taxonomy.yaml', 'rb') as yamlfile:
    genres = yaml.load(yamlfile)
    for genre in genres:
        print 'genre:',genre['key']
        genre_dir = os.path.join(sub_dir,genre['key'])
        if not os.path.exists(genre_dir):
            os.makedirs(genre_dir)
        for subgenre in genre['subtags']:
            print 'subgenre',subgenre['key']
            subgenre_dir = os.path.join(genre_dir,subgenre['key'])
            if not os.path.exists(subgenre_dir):
                os.makedirs(subgenre_dir)
            for subsubgenre in subgenre['subtags']:
                print 'subsubgenre',subsubgenre['key']
                subsubgenre_dir = os.path.join(subgenre_dir,subsubgenre['key'])
                if not os.path.exists(subsubgenre_dir):
                    os.makedirs(subsubgenre_dir)