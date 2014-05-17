from tagger.postagger import brown_tag, tag_index
from sentiment.swnreader import SWNReader
from preproc.spell_check import correct
from preproc.filter import base_filter, concat_rows
from reader.csv_reader import CSVFile
import os
import shutil
import csv

allstags = {'a', 'r', 'v', 'n'}

sub_dir1 = 'D:/Dropbox/Work/Sound Cloud/Data/train/dubstep'
sub_dir2 = 'D:/Dropbox/Work/Sound Cloud/Data/train/dubstep/new'
sub_dir3 = 'D:/Dropbox/Work/Sound Cloud/Data/train/dubstep/senti'

swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
swn = SWNReader(swn_filename)

if os.path.exists(sub_dir2):
    shutil.rmtree(sub_dir2)
if os.path.exists(sub_dir3):
    shutil.rmtree(sub_dir3)

for filename in os.listdir(sub_dir1):
    r_file = CSVFile(filename, sub_dir1)
    r_file.readcsv()
    r_rows = r_file.rows
    r_rows = concat_rows(r_rows)
    r_rows = base_filter(r_rows)
    
    w_rows = []
    
    for row in r_rows:
        tot_score = 0
        useful = 0
        feats = []
        tags = brown_tag(row[1])
        stags = tag_index(tags)
        for i,stag in enumerate(stags):
            if stag[1] not in allstags:
                try:
                    pos_score, neg_score = swn.no_pos_senti_synset(stag[0])
                except TypeError:
                    pos_score = neg_score = 0
                obj = 1 - (float(pos_score) + float(neg_score))
                tot_score = tot_score + float(pos_score) - float(neg_score)
                if obj != 1:
                    useful = useful + 1
                    feats.append(stag[0])
            else:
                try:
                    pos_score, neg_score = swn.senti_synset(stag[0] + '.' + stag[1] + '.' + '1')
                except TypeError:
                    pos_score = neg_score = 0
                obj = 1 - (float(pos_score) + float(neg_score))
                tot_score = tot_score + float(pos_score) - float(neg_score)
                if obj != 1:
                    useful = useful + 1
                    feats.append(stag[0])
        if useful != 0:
            net_score = tot_score/useful
        else:
            net_score = 0
        row.append(net_score)
        row.append(feats)
        #print row, useful
        w_rows.append(row)
    
    
    w_file = CSVFile('new_' + filename, sub_dir2)
    w_file.writecsv(w_rows)