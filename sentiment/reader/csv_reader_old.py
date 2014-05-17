#!/usr/bin/env python
import csv
import os
import re
import nltk

def writecsv(sub_dir2, sub_dir3, filename, nrow):
    if not os.path.exists(sub_dir3):
        os.makedirs(sub_dir3)
    wf = open(os.path.join(sub_dir2, filename), 'wb')
    writer = csv.writer(wf, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    rf = open(os.path.join(sub_dir2, filename), "r")
    reader = csv.reader(rf)
    for row in reader:
        writer.writerow(nrow)

def readcsv(sub_dir2, filename):
    rf = open(os.path.join(sub_dir2, filename), "r")
    reader = csv.reader(rf)
    for row in reader:
        return row
    #rf.close()

def preproc(sub_dir, sub_dir2, filename):
    #for filename in os.listdir(sub_dir):
    if not os.path.exists(sub_dir2):
        os.makedirs(sub_dir2)
    wf = open(os.path.join(sub_dir2, filename), 'wb')
    writer = csv.writer(wf, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    rf = open(os.path.join(sub_dir, filename), "r")
    reader = csv.reader(rf)
    for row in reader:
        #concat strings containing commas
        if len(row)>2:
            for i in row:
                if i != row[0] and i != row[1]:
                    row.remove(i)
                    #temp = row[1]
                    #row.pop(1)
                    row[1] = row[1] + ' ' + i


        #remove spam and noise
        if not any('http' in s for s in row) and row != [] and not any('\xc3' in s for s in row):
            writer.writerow(row)
    #rf.close()
    #wf.close()