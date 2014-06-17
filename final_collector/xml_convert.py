#!/usr/bin/env python
#!/usr/bin/env python
import os
import cPickle as pickle
import math
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from preproc.filter import remove_diacritic, check_exist
import nltk
import re
import lxml.etree as et
import StringIO

s = """<?xml version="1.0" encoding = "utf-8"?>"""
sub_dir1 = '/home/sathya/Dev/soundcloud-data/bulk_pickle'
sub_dir2 = '/home/sathya/Dev/soundcloud-data/bulk_xml'


with open('xml_log.tsv', 'wb') as logfile:
    logwriter = csv.writer(logfile, delimiter = '\t')
    for root1, dirs, files in os.walk(sub_dir1):
            for filename in files:
                if '.track' in filename:
                    track_dir = os.path.join(root1, filename)
                    with open(track_dir, 'rb') as track_input:
                        track = pickle.load(track_input)
                    try:
                        file_index = int(math.ceil(track.comment_count/200))
                    except:
                        file_index = 0
                    id_ = track.id
                    genre = os.path.relpath(root1,sub_dir1)
                    if(track.genre):
                        owner_genre = track.genre
                    else:
                        owner_genre = ''
                    tag_list = []
                    tags = ''
                    for word in nltk.regexp_tokenize(track.tag_list, pattern=r'(\s+)', gaps = True):
                        tag_list.append(word)
                    quoted = 0
                    try:
                        for tag in tag_list:
                            tag = tag.strip()
                            tag = re.sub(',','', tag)
                            if '"' not in tag[0] and not(quoted):
                                tags = tags + check_exist(tag) + ', '
                            else:
                                quoted = 1
                                tags = tags + check_exist(tag) + ' '
                                if '"' in tag[len(tag)-1]:
                                    tags = tags.rstrip()
                                    quoted = 0
                                    tags = tags + ', '
                        #tags = re.sub('"','\'', tags)
                        if(tags):
                            tags = tags[:-2]
                    except Exception, e:
                        tags = ''
                        #print str(e)
                        logrow = [track.id, str(e)]
                        logwriter.writerow(logrow)
                    root2 = sub_dir2 + '/' + genre
                    if not os.path.exists(root2):
                        os.makedirs(root2)
                    xml_filename = str(id_) + '.xml'
                    xml_dir = os.path.join(root2, xml_filename)
                    with open(xml_dir, 'wb') as xml_file:
                        sound = Element('sound')
                        track_xml = SubElement(sound, 'track',
                                           {'track_id' :str(track.id),
                                            'created_at' :str(track.created_at),
                                            'user_id' :str(track.user_id),
                                            'title' :check_exist(track.title),
                                            'permalink' :str(track.permalink),
                                            'track_permalink_url' :str(track.permalink_url),
                                            'uri' :str(track.uri),
                                            'sharing' :str(track.sharing),
                                            'embeddable_by' :str(track.embeddable_by),
                                            'purchase_url' :str(track.purchase_url),
                                            'artwork_url' :str(track.artwork_url),
                                            'description' :check_exist(track.description),
                                            'label' :str(track.label),
                                            'duration' :str(track.duration),
                                            'owner_genre' :owner_genre,
                                            'classified_genre':str(genre),
                                            'shared_to_count' :str(track.shared_to_count),
                                            'tag_list' :tags,
                                            'label_id' :str(track.label_id),
                                            'label_name' :check_exist(track.label_name),
                                            'release' :check_exist(track.release),
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
                            comment_count = 0
                            try:
                                with open(comment_dir, 'rb') as comment_in:
                                    comments = pickle.load(comment_in)
                                for comment in reversed(comments):
                                    comment_count += 1
                                    comment_xml = SubElement(sound, 'comment',
                                                             {'comment_id' :str(comment.id),
                                                              'comment_uri' :str(comment.uri),
                                                              'commented_at' :str(comment.created_at),
                                                              'body' :comment.body,
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
                                                           'username' :  comment.user['username'],
                                                           'permalink' : str(comment.user['permalink']),
                                                           'kind' : str(comment.user['kind']),
                                                           'user_uri' : str(comment.user['uri']),
                                                           'avatar_url' : str(comment.user['avatar_url']),
                                                           'user_permalink_url' : str(comment.user['permalink_url']),
                                                           'user_id' : str(comment.user['id'])
                                                          })
                            except Exception, e:
                                #print str(e)
                                logrow = [track.id, str(e)]
                                logwriter.writerow(logrow)
                                break
                        track_xml.set('comment_count' ,str(comment_count))
                        #print prettify(sound)
                        xml_file.write(s)
                        tree = ElementTree(sound)
                        tree.write(xml_file)
