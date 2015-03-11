#!/usr/bin/env python
from __future__ import division
import csv
from numpy import cumsum
import collections

comment_count_dict = {}
count_array = []
percent_dict = {}
cumpercent_dict = {}
with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/favorites/comment-count.tsv', 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter = '\t')
    for row in tsvreader:
        if int(row[1]) not in comment_count_dict:
            comment_count_dict[int(row[1])] = 0
        comment_count_dict[int(row[1])] += 1
        count_array.append(int(row[1]))

sorted_dict = collections.OrderedDict(sorted(comment_count_dict.items()))
keys = sorted_dict.keys()
values = sorted_dict.values()
total = sum(values)

percent_dict = dict(zip(keys, (100*val/total for val in values)))
percent_dict = collections.OrderedDict(sorted(percent_dict.items()))
cumpercent_dict = dict(zip(list(reversed(keys)), (100*val/total for val in cumsum(list(reversed(values))))))
cumpercent_dict = collections.OrderedDict(sorted(cumpercent_dict.items()))
cumsum_dict = dict(zip(list(reversed(keys)), (val for val in cumsum(list(reversed(values))))))
cumsum_dict = collections.OrderedDict(sorted(cumsum_dict.items()))

with open('count_percent.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    for key in percent_dict:
        tsvwriter.writerow([key, percent_dict[key]])

with open('count_cumpercent.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    for key in cumpercent_dict:
        tsvwriter.writerow([key, cumpercent_dict[key]])

with open('count_cumsum.tsv', 'w') as newtsvfile:
    tsvwriter = csv.writer(newtsvfile, delimiter = '\t')
    for key in cumsum_dict:
        tsvwriter.writerow([key, cumsum_dict[key]])