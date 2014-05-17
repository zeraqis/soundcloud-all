#!/usr/bin/env python
import csv
import os
import re
import nltk

class CSVFile:
    def __init__(self, filename, sub_dir):
        self.filename = filename
        self.sub_dir = sub_dir
        self.rows = []

    def writecsv(self, nrows):
        if not os.path.exists(self.sub_dir):
            os.makedirs(self.sub_dir)
        wf = open(os.path.join(self.sub_dir, self.filename), 'wb')
        writer = csv.writer(wf, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for nrow in nrows:
            writer.writerow(nrow)
    
    def readcsv(self):
        rf = open(os.path.join(self.sub_dir, self.filename), "r")
        reader = csv.reader(rf)
        for row in reader:
            self.rows.append(row)