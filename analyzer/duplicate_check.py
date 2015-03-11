#!/usr/bin/env python
import csv

tracks = []
with open('timed-comments-data.tsv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] not in tracks:
            tracks.append(row[0])
        else:
            print row[0]
print len(tracks)