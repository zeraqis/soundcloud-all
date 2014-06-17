#!/usr/bin/env python
from xml.etree.ElementTree import XML

with open('102378368.xml') as xmlfile:
    reader = xmlfile.read()
    e = XML(reader)
    track = e.find('track')
    print(track.get('created_at'))
    comments = e.findall('comment')
    for comment in comments:
        for user in comment.findall('user'):
            print(user.get('username'))