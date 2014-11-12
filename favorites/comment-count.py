#!/usr/bin/env python
import csv
import ast

count = 0
with open('comment-count.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    with open('track-user.tsv', 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter = '\t')
        for row in tsvreader:
            commentlist = ast.literal_eval(row[1])
            count = count + len(commentlist)
            tsvwriter.writerow([row[0], len(commentlist)])
print count