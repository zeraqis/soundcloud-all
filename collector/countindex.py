#!/usr/bin/env python
import soundcloud
from preproc.filter import remove_diacritic
import unicodedata
import cPickle as pickle
import datetime

licenses = [
    'no-rights-reserved',
    'all-rights-reserved',
    'cc-by',
    'cc-by-nc',
    'cc-by-nd',
    'cc-by-sa',
    'cc-by-nc-nd',
    'cc-by-nc-sa'
]

no_rights_reserved= 0
all_rights_reserved= 0
cc_by= 0
cc_by_nc= 0
cc_by_nd= 0
cc_by_sa= 0
cc_by_nc_nd= 0
cc_by_nc_sa= 0

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
    "other",
    "none"
]

original = 0
remix = 0
live = 0
recording = 0
spoken = 0
podcast = 0
demo = 0
in_progress = 0
stem = 0
loop = 0
sound_effect = 0
sample = 0
other = 0
none = 0

req_genres = [
    "Alternative Rock",
    "Ambient",
    "Classical",
    "Country",
    "Dance",
    "Deep House",
    "Disco",
    "Drum & Bass",
    "Dubstep",
    "Electro",
    "Electronic",
    "Folk",
    "Hardcore Techno",
    "Hip Hop",
    "House",
    "Indie Rock",
    "Jazz",
    "Latin",
    "Metal",
    "Minimal Techno",
    "Piano",
    "Pop",
    "Progressive House",
    "Punk",
    "R&B",
    "Rap",
    "Reggae",
    "Rock",
    "Singer-Songwriter",
    "Soul",
    "Tech House",
    "Techno",
    "Trance",
    "Trap",
    "Trip Hop",
    "World",
    "Audiobooks",
    "Business",
    "Comedy",
    "Entertainment",
    "Learning",
    "News & Politics",
    "Religion & Spirituality",
    "Science",
    "Sports",
    "Storytelling",
    "Technology"
]

temp = [
    'cc-by-nc-sa',
    'cc-by'
    ]

client = soundcloud.Client(client_id='68b18cab0f8633ff354b6c19296b5b5d')
created_to = datetime.datetime(2014, 01, 01, 00, 00, 00)
n = datetime.timedelta(0,120)
created_to = created_to - n
print created_to
r_tracks = client.get('/tracks', limit=10, genres = 'singer-songwriter', license =temp)

for track in r_tracks:
    print track.license
    if track.track_type == track_types[4]:
        print track.title
    if track.track_type == track_types[0]:
        original += 1
    if track.track_type == track_types[1]:
        remix += 1
    if track.track_type == track_types[2]:
        live += 1
    if track.track_type == track_types[3]:
        recording += 1
    if track.track_type == track_types[4]:
        spoken += 1
    if track.track_type == track_types[5]:
        podcast += 1
    if track.track_type == track_types[6]:
        demo += 1
    if track.track_type == track_types[7]:
        in_progress += 1
    if track.track_type == track_types[8]:
        stem += 1
    if track.track_type == track_types[9]:
        loop += 1
    if track.track_type == track_types[10]:
        sound_effect += 1
    if track.track_type == track_types[11]:
        sample += 1
    if track.track_type == track_types[11]:
        other += 1
    if track.track_type == track_types[12]:
        none += 1
        
    if track.license == licenses[0]:
        no_rights_reserved += 1
    if track.license == licenses[1]:
        all_rights_reserved += 1
    if track.license == licenses[2]:
        cc_by += 1
    if track.license == licenses[3]:
        cc_by_nc += 1
    if track.license == licenses[4]:
        cc_by_nd += 1
    if track.license == licenses[5]:
        cc_by_sa += 1
    if track.license == licenses[6]:
        cc_by_nc_nd += 1
    if track.license == licenses[7]:
        cc_by_nc_sa += 1

print "no_rights_reserved" ,no_rights_reserved, "all_rights_reserved", all_rights_reserved, "cc_by", cc_by
print "cc_by_nc", cc_by_nc,  "cc_by_nd", cc_by_nd, "cc_by_sa", cc_by_sa,  "cc_by_nc_nd", cc_by_nc_nd,  "cc_by_nc_sa", cc_by_nc_sa

print "original",  original,  "remix", remix,  "live", live, "recording" , recording, "spoken", spoken
print "podcast", podcast ,"demo", demo ,"in_progress", in_progress ,"stem", stem ,"loop", loop ,"sound_effect", sound_effect ,"sample", sample
print "other", other, "none" , none