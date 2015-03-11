#!/usr/bin/env python
import csv
import ast

comment_count = 0
track_count = 0
with open('comment-count.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    with open('comments_track-user.tsv', 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter = '\t')
        for row in tsvreader:
            track_count += 1
            commentlist = ast.literal_eval(row[1])
            comment_count = comment_count + len(commentlist)
            tsvwriter.writerow([row[0], len(commentlist)])
with open('count-report', 'w') as newfile:
    newfile.write('COMMENTED TRACK COUNT : ' + str(track_count) + '\n')
    newfile.write('COMMENT COUNT : ' + str(comment_count))