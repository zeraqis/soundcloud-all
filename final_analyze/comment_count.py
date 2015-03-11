#!/usr/bin/env python
from __future__ import division
import csv
from numpy import cumsum
import collections
import json

with open('/tudelft.net/staff-bulk/ewi/insy/mmc/nathan/souncloud-all/favorites/comments_track-user.json', 'r') as jsonfile:
    track_user_dict = json.load(jsonfile)
    for track in track_user_dict:
        print track