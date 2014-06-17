#!/usr/bin/env python
import csv

newrows = []
count = 0
t = 1
with open('timed-comments-data.tsv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter = '\t')
    for row in reader:
        count += 1
        row.append(t)
        newrows.append(row)
        if count % 50000 == 0:
            with open('timed-comments-data' + '_' + str(t), 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter = '\t')
                for row in newrows:
                    writer.writerow(row)
            newrows = []
            t += 1
with open('timed-comments-data' + '_' + str(t), 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = '\t')
    for row in newrows:
        writer.writerow(row)
