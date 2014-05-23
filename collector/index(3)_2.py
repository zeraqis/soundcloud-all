#!/usr/bin/env python
#!/usr/bin/env python
#!/usr/bin/env python
import soundcloud
from preproc.filter import remove_diacritic
import unicodedata
import cPickle as pickle
import os
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


req_genres = [
    "alternative rock",
    "ambient",
    "classical",
    "country",
    "dance",
    "deep house",
    "disco",
    "drum & bass",
    "dubstep",
    "electro",
    "electronic",
    "folk",
    "hardcore techno",
    "hip hop",
    "house",
    "indie rock",
    "jazz",
    "latin",
    "metal",
    "minimal techno",
    "piano",
    "pop",
    "progressive house",
    "punk",
    "r&b",
    "rap",
    "reggae",
    "rock",
    "singer-songwriter",
    "soul",
    "tech house",
    "techno",
    "trance",
    "trap",
    "trip hop",
    "world",
]

for req_genre in req_genres:

    sub_dir = 'data/cc-by-nc-nd/' + req_genre + '/'
    
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    
    client = soundcloud.Client(client_id='68b18cab0f8633ff354b6c19296b5b5d')
    pages = 0
    while pages < 8200:
        try:
            r_tracks = client.get('/tracks', limit = 200, offset = pages,  created_at = { 'from' : '2012-06-01 00:00:00' , 'to' : '2013-01-01 00:00:00'}, genre = req_genre, license = 'cc-by-nc-nd', order='created_at')
            if not(r_tracks):
                break
            for track in r_tracks:
                try:
                    #print track.id
                    if track.comment_count:
                        track_filename = sub_dir + str(track.id) + '.track'
                        with open(track_filename, 'wb') as output:
                            pickle.dump(track, output, -1)
                        comment_pages = 0
                        n = 0
                        while comment_pages < 8200:
                            r_comments = client.get('/tracks/' + str(track.id) + '/comments', limit = 200, offset = comment_pages)
                            n += 1
                            if not(r_comments):
                                break
                            comment_filename = sub_dir + str(track.id) + '_' + str(n)  + '.comment'
                            with open(comment_filename, 'wb') as output:
                                pickle.dump(r_comments, output, -1)
                            comment_pages += 200
                except:
                    print "No Comment:", track.id
            pages += 200
        except:
            print "503"

#!/usr/bin/env python

