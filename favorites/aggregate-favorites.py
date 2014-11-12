#!/usr/bin/env python
import csv

user_fav_dict = {}
for i in range(1,33):
    filename = "user-favorite-" + str(i) + ".tsv"
    with open(filename, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter = '\t')
        for row in tsvreader:
            user = row[0]
            if user not in user_fav_dict:
                user_fav_dict[user] = row[1]
                #print user, user_fav_dict[user]
with open("user-favorites.tsv",'w') as bulktsv:
    tsvwriter = csv.writer(bulktsv, delimiter = '\t')
    for user in user_fav_dict:
        tsvwriter.writerow([user, user_fav_dict[user]])