#!/usr/bin/env python
import os
import re
import cPickle as pickle

sub_dir1 = "final"
sub_dir2 = "txt"

if not os.path.exists(sub_dir2):
        os.makedirs(sub_dir2)

for lic_folder in os.listdir(sub_dir1):
    lic_dir = sub_dir1 + '/' + str(lic_folder)
    for genre_folder in os.listdir(lic_dir):
        genre_dir = lic_dir + '/' + str(genre_folder)
        for filename in os.listdir(genre_dir):
            if '.comment' in filename:
                file_dir = genre_dir + '/' + str(filename)
                with open(file_dir, 'rb') as input:
                    comments = pickle.load(input)
                    p = re.compile('comment')
                    txt_file = p.sub('txt', filename)
                    txt_folder = sub_dir2 + '/' + str(lic_folder) + '/' + str(genre_folder)
                    txt_dir = sub_dir2 + '/' + str(lic_folder) + '/' + str(genre_folder) + '/' + str(txt_file)
                    if not os.path.exists(txt_folder):
                        os.makedirs(txt_folder)
                    with open(txt_dir, 'wb') as txt_writer:
                        for comment in comments:
                            #print comment.body
                            txt_writer.write(str(comment.id) + '\t' + str(comment.created_at) + '\t'
                                             + comment.body.encode('utf-8').strip() + '\t' + str(comment.timestamp) + '\n')