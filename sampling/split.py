#!/usr/bin/env python
import json
import csv
from datetime import datetime

train_time = datetime.strptime("2013/01/01 00:00:00 +0000"[:-6], "%Y/%m/%d %H:%M:%S")
dev_time = datetime.strptime("2013/04/01 00:00:00 +0000"[:-6], "%Y/%m/%d %H:%M:%S")
print train_time
print dev_time

train_dict = {}
dev_dict = {}

with open("comments_track-user-timed.json", "r") as big_json:
    big_dict = json.load(big_json)
    for a in big_dict:
        for b in big_dict[a]:
            for time in big_dict[a][b]:
                curr_time = datetime.strptime(time[:-6], "%Y/%m/%d %H:%M:%S")
                if curr_time < train_time:
                    if a not in train_dict:
                        train_dict[a] = {}
                    if b not in train_dict[a]:
                        train_dict[a][b] = {}
                    train_dict[a][b][time] = big_dict[a][b][time]
                if curr_time > train_time and curr_time < dev_time:
                    if a not in dev_dict:
                        dev_dict[a] = {}
                    if b not in dev_dict[a]:
                        dev_dict[a][b] = {}
                    dev_dict[a][b][time] = big_dict[a][b][time]

with open('dev_users.tsv', 'w') as tsv_file:
    tsvwriter = csv.writer(tsv_file, delimiter = '\t')
    for dev_track in dev_dict:
        for dev_user in dev_dict[dev_track]:
            tsvwriter.writerow([dev_user])


with open("timed_train.json","w") as train_json_file:
    json.dump(train_dict, train_json_file, indent=4)
    
with open("timed_dev.json","w") as dev_json_file:
    json.dump(dev_dict, dev_json_file, indent=4)