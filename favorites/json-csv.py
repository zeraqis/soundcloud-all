#!/usr/bin/env python
import json
import csv
#from eta import ETA

with open('user-interaction.json', 'r') as jsonfile:
    interactions = json.load(jsonfile)
    
with open('interaction-counts.csv', 'w') as csvfile:
    print 'JSON Loaded'
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['user', '#comment_and_favorite', '%comment_and_favorite', '#comment_and_not_favorite', '#comments', '#favorites'])
    #eta = len(interactions)
    for user in interactions:
        csvwriter.writerow([user, interactions[user]['stats']['comment_and_favorite_count'], interactions[user]['stats']['percent'],
                            interactions[user]['stats']['comment_and_not_favorite_count'], interactions[user]['stats']['comment_count'], interactions[user]['stats']['favorite_count']])
        #eta.print_status()
#eta.done()
