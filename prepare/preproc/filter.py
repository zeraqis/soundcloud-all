#!/usr/bin/env python
import unicodedata
import string

def concat_rows(rows):
    for row in rows:
        #concat strings containing commas
        if len(row)>2:
            for i in row:
                if i != row[0] and i != row[1]:
                    row.remove(i)
                    #temp = row[1]
                    #row.pop(1)
                    row[1] = row[1] + ' ' + i
    return rows


def remove_diacritic(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    if input:
        return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')
    else:
        return ''

def check_exist(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    if input:
        return input
    else:
        return ''

def replace_diacritic(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    if input:
        return input.encode('ASCII', 'xmlcharrefreplace')
    else:
        return ''

def remove_punctuation(x):
    exclude = set(string.punctuation)
    x = ''.join(ch for ch in x if ch not in exclude)
    return x

def base_filter(rows):
    nrows = []
    for row in rows:
        if not any('http' in s for s in row) and row != [] and len(row)==2:
            x = row[1]
            row.remove(row[1])
            x = remove_diacritic(unicode(x, 'ISO-8859-1'))
            x = x.lower()
            exclude = set(string.punctuation)
            x = ''.join(ch for ch in x if ch not in exclude)
            row.append(x)
            nrows.append(row)
    return nrows
