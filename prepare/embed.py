#!/usr/bin/env python
from xml.etree.ElementTree import XML
import os
import nltk
import csv

sub_dir = '/home/sathya/Dev/soundcloud-data/xml_original_final'
with open('embed.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    for root, dirs, files in os.walk(sub_dir):
        for filename in files:
            file_dir = os.path.join(root, filename)
            with open(file_dir, 'rb') as xmlfile:
                reader = xmlfile.read()
                e = XML(reader)
                track = e.find('track')
                id_ = track.get('track_id')
                uri = track.get('uri')
                embed = track.get('embeddable_by')
                row = [id_,uri,embed]
                csvwriter.writerow(row)