#!/usr/bin/env python
import csv

user_err_dict = {}
for i in range(1,33):
    filename = "erroneous-" + str(i) + ".tsv"
    with open(filename, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter = '\t')
        for row in tsvreader:
            user = row[0]
            if user not in user_err_dict:
                user_err_dict[user] = row[1]
                #print user, user_err_dict[user]
with open("erroneous.tsv",'w') as bulktsv:
    tsvwriter = csv.writer(bulktsv, delimiter = '\t')
    for user in user_err_dict:
        tsvwriter.writerow([user, user_err_dict[user]])