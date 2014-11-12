#!/usr/bin/env python
from xml.etree.ElementTree import XML
import os

sub_dir ='/home/sathya/Dev/soundcloud-data/xml_original_final/'
count = 0
for root, dirs, files in os.walk(sub_dir):
        for xml_filename in files:
            xml_filedir = os.path.join(root,xml_filename)
            with open(xml_filedir, 'rb') as xml_file:
                reader = xml_file.read()
                e = XML(reader)
                track = e.find('track')
                print(track.get('created_at'))
                comments = e.findall('comment')
                for comment in comments:
                    if "drop" or "drop" or "drops" or "dropped" or "dropping" or "droppin" in comment.get('body'):
                        count = count + 1
print count