#!/usr/bin/env python
import os
import cPickle as pickle
import math
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml_pretty import prettify
from preproc.filter import remove_diacritic

sub_dir1 = '/home/sathya/Dev/soundcloud-data/categorized'
sub_dir2 = '/home/sathya/Dev/soundcloud-data/categorized_comments'
with open('relative_week.csv', 'rb') as track_file:
    reader = csv.reader(track_file)
    for row in reader:
        id_ = row[0]
        license = row[2]
        genre = row[3]
        root1 = sub_dir1 + '/' + license + '/' + genre
        root2 = sub_dir2 + '/' + license + '/' + genre
        if not os.path.exists(root2):
            os.makedirs(root2)
        xml_filename = id_ + '.xml'
        xml_dir = os.path.join(root2, xml_filename)
        track_filename = id_ + '.track'
        track_dir = os.path.join(root1, track_filename)
        with open(track_dir, 'rb') as track_input:
            track = pickle.load(track_input)
        file_index = int(math.ceil(track.comment_count/200))
        with open(xml_dir, 'wb') as xml_file:
            sound = Element('sound')
            track_xml = SubElement(sound, 'track',
                               {'id' :str(track.id),
                                'created_at' :str(track.created_at),
                                'user_id' :str(track.user_id),
                                'title' :remove_diacritic(track.title),
                                'permalink' :str(track.permalink),
                                'permalink_url' :str(track.permalink_url),
                                'uri' :str(track.uri),
                                'sharing' :str(track.sharing),
                                'embeddable_by' :str(track.embeddable_by),
                                'purchase_url' :str(track.purchase_url),
                                'artwork_url' :str(track.artwork_url),
                                'description' :remove_diacritic(track.description),
                                'label' :str(track.label),
                                'duration' :str(track.duration),
                                'genre' :str(track.genre),
                                'shared_to_count' :str(track.shared_to_count),
                                'tag_list' :track.tag_list,
                                'label_id' :str(track.label_id),
                                'label_name' :remove_diacritic(track.label_name),
                                'release' :remove_diacritic(track.release),
                                'release_day' :str(track.release_day),
                                'release_month' :str(track.release_month),
                                'release_year' : str(track.release_year),
                                'streamable' :str(track.streamable),
                                'downloadable' :str(track.downloadable),
                                'state' :str(track.state),
                                'license' :str(track.license),
                                'track_type' :str(track.track_type),
                                'waveform_url' :str(track.waveform_url),
                                'download_url' :str(track.download_url),
                                'stream_url' :str(track.stream_url),
                                'bpm' :str(track.bpm),
                                'commentable' :str(track.commentable),
                                'isrc' :str(track.isrc),
                                'key_signature' :str(track.key_signature),
                                'comment_count' :str(track.comment_count),
                                'download_count' :str(track.download_count),
                                'playback_count' :str(track.playback_count),
                                'favoritings_count' :str(track.favoritings_count),
                                'original_format' :str(track.original_format),
                                'original_content_size' :str(track.original_content_size),
                                'created_with' :str(track.created_with),
                                'asset_data' :str(track.asset_data),
                                'artwork_data' :str(track.artwork_data),
                                'user_favorite' :str(track.user_favorite),
                               })
            if file_index == 0:
                file_index = 1
            for i in range(file_index):
                comment_filename = str(id_) + '_' + str(i+1) +'.comment'
                comment_dir = os.path.join(root1, comment_filename)
                with open(comment_dir, 'rb') as comment_in:
                    comments = pickle.load(comment_in)
                    for comment in reversed(comments):
                        if comment.timestamp:
                            try:
                                comment.body.decode('ascii')
                            except UnicodeEncodeError:
                                a = 1
                            else:
                                if len(comment.body) > 1 and 'http' not in comment.body and comment.user_id != track.user_id:
                                    comment_xml = SubElement(sound, 'comment',
                                                             {'id' :str(comment.id),
                                                              'uri' :str(comment.uri),
                                                              'created_at' :str(comment.created_at),
                                                              'body' :str(comment.body),
                                                              'timestamp' :str(comment.timestamp),
                                                              #'user_id' :str(comment.user_id),
                                                              #'user' :str(comment.user),
                                                              'track_id' :str(comment.track_id)
                                                             })
                                    #tmp = []
                                    #for item in comment.user:
                                    #    try:
                                    #        tmp.append(remove_diacritic(comment.user[item]))
                                    #    except:
                                    #        tmp.append(str(comment.user[item]))
                                    user_xml = SubElement(comment_xml, 'user',
                                                          {
                                                           'username' :  remove_diacritic(comment.user['username']),
                                                           'permalink' : str(comment.user['permalink']),
                                                           'kind' : str(comment.user['kind']),
                                                           'uri' : str(comment.user['uri']),
                                                           'avatar_url' : str(comment.user['avatar_url']),
                                                           'permalink_url' : str(comment.user['permalink_url']),
                                                           'id' : str(comment.user['id'])
                                                          })
            #print prettify(sound)
            tree = ElementTree(sound)
            tree.write(xml_file)