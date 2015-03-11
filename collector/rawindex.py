#!/usr/bin/env python
import soundcloud
from preproc.filter import remove_diacritic
import unicodedata
import cPickle as pickle
import os

licenses = [
    'no-rights-reserved',
    #'all-rights-reserved',
    'cc-by',
    'cc-by-nc',
    'cc-by-nd',
    'cc-by-sa',
    'cc-by-nc-nd',
    'cc-by-nc-sa'
]

track_types = [
    "original",
    "remix",
    "live",
    "recording",
    "spoken",
    "podcast",
    "demo",
    "in progress",
    "stem",
    "loop",
    "sound effect",
    "sample",
    "other"
]

client = soundcloud.Client(client_id='68b18cab0f8633ff354b6c19296b5b5d')
r_tracks = client.get('/tracks/127011388')
print r_tracks.permalink_url