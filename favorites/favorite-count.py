#!/usr/bin/env python
import csv
import ast

count = 0
with open('favorite-count.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    with open('user-favorites.tsv', 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter = '\t')
        for row in tsvreader:
            favoritelist = ast.literal_eval(row[1])
            count = count + len(favoritelist)
            tsvwriter.writerow([row[0], len(favoritelist)])
print count