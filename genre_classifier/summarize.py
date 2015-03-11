#!/usr/bin/env python
import csv
import os

sub_dir = 'per-user'
with open('summary_user.results', 'w') as summary:
    summary_writer = csv.writer(summary, delimiter='\t')
    summary_writer.writerow(['file', 'featx', 'selection', 'precision', 'recall', 'f_score'])
    for root, dirs, files in os.walk(sub_dir):
        for resultfile in files:
            if 'results' in resultfile and 'label' not in resultfile:
                file_dir = os.path.join(root, resultfile)
                with open(file_dir, 'r') as tsvfile:
                    tsvreader = csv.reader(tsvfile, delimiter='\t')
                    for row in tsvreader:
                        results = row
                    newrow = []
                    newrow.append(resultfile)
                    if 'count' in resultfile:
                        newrow.append('term_freq')
                    if 'tfidf' in resultfile:
                        newrow.append('tf_idf')
                    if 'select' in resultfile:
                        newrow.append('yes')
                    else:
                        newrow.append('no')
                    newrow.extend(results)
                    print newrow
                    if newrow != []:
                        summary_writer.writerow(newrow)
