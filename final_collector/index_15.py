#!/usr/bin/env python
#!/usr/bin/env python
import soundcloud
import unicodedata
import cPickle as pickle
import os
import datetime
import csv
import itertools
import sys
import traceback

client = soundcloud.Client(client_id='68b18cab0f8633ff354b6c19296b5b5d')
pages = 0
sub_dir = '/home/sathya/Dev/soundcloud-data/bulk_pickle'
with open('erroneous_15.tsv', 'wb') as errfile:
    errwriter = csv.writer(errfile, delimiter = '\t')
    with open('timed-comments-data_15', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        for row in reader:
            try:
                track = client.get('/tracks/' + str(row[0]).strip())
                #print track.id, row[0], row[6]
                genres = row[6].split(',')
                tmp =[]
                for genre in genres:
                    tmp.append(genre + '/')
                #genre_combos = []
                genre_combos = list(itertools.permutations(tmp))
                genre_dirs = []
                for genre_combo in genre_combos:
                    genre_dirs.append(''.join(genre_combo)[:-1])
                with open('dirs.txt', 'rb') as txtfile:
                    txtreader = txtfile.readlines()
                    for line in txtreader:
                        for genre_dir in genre_dirs:
                            #print genre_dir, line
                            if str(genre_dir).strip() == str(line).strip():
                                #print genre_dir, line
                                curr_dir = os.path.join(sub_dir,genre_dir)
                try:
                #print track.id
                    track_filename = curr_dir + '/' + str(track.id) + '.track'
                    with open(track_filename, 'wb') as output:
                        pickle.dump(track, output)
                    comment_pages = 0
                    n = 0
                    while comment_pages < 8200:
                        r_comments = client.get('/tracks/' + str(row[0]).strip() + '/comments', limit = 200, offset = comment_pages)
                        n += 1
                        if not(r_comments):
                            break
                        comment_filename = curr_dir + '/' + str(track.id) + '_' + str(n)  + '.comment'
                        #print comment_filename
                        with open(comment_filename, 'wb') as output:
                            pickle.dump(r_comments, output)
                        comment_pages += 200
                except Exception,e:
                    print str(e)
                    traceback.print_exc()
                    err = [row[0], str(e)]
                    errwriter.writerow(err)
            except Exception,e:
                print str(e)
                err = [row[0], str(e)]
                errwriter.writerow(err)
            #break
