#!/usr/bin/env python
import os
import cPickle as pickle
import csv
import ast
import soundcloud
import traceback
import sys
from eta import ETA

user_favorite_dict = {}
client = soundcloud.Client(client_id='68b18cab0f8633ff354b6c19296b5b5d')

with open('erroneous-11.tsv', 'wb') as errfile:
    errwriter = csv.writer(errfile, delimiter = '\t')
    with open('xak','r') as tsvfile:
        eta =  ETA(10000)
        tsvreader = csv.reader(tsvfile, delimiter = '\t')
        for row in tsvreader:
            userlist = ast.literal_eval(row[1])
            for user in userlist:
                eta.print_status()
                if user not in user_favorite_dict:
                    #print user
                    user_favorite_dict[user] = []
                    try:
                        favorites = client.get('/users/' + str(user).strip() + '/favorites')
                        for favorite in favorites:
                            user_favorite_dict[user].append(favorite.id)
                    except Exception,e:
                        #print str(e)
                        err = [user, str(e)]
                        errwriter.writerow(err)
    with open('user-favorite-11.tsv','w') as newtsvfile:
        tsvwriter = csv.writer(newtsvfile, delimiter='\t')
        for user in user_favorite_dict:
            tsvwriter.writerow([user, user_favorite_dict[user]])