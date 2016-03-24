#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import csv
from html import unescape
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from TweetStore import TweetStore
from vectorization import Vectorizer


URL = re.compile(r'(https?)?:\/\/(\w\.\w.)\/\w*')
COUCH_SERVER = 'http://192.168.1.106:5984/'


# fuction that flattens the dictionary structure
def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items()) 
        else:
            items.append((new_key, v))
    return dict(items)


# function that strips out unnecessary stuff
def prep_txt(txt):
    try:
        txt = unescape(txt)
        txt = re.sub(URL, '', txt)
        return ''.join([w for w in txt if w.isalnum() or w.isspace()])
    except:
        pass


# maps a series onto another series
def createMap(k_series, v_series):
    keys = list(k_series)
    vals = list(v_series)
    
    return dict({(i,n) for i, n in zip(keys, vals)})


# calculate the center of a bounding box of coordinates
def center(b_box, rev=True):
    box = [x for y in b_box for x in y]
    c = list(map(lambda x: x/4, [sum(x) for x in zip(box[0], box[1], box[2], box[3])]))
    # for geojson format
    if rev:
        c.reverse()
    else:
        pass

    return list(c)


def getDF(db_name, server):
    db = TweetStore(db_name, server)
    tweets = [flatten(dict(t)) for t in db.get_tweets()]
    df = pd.DataFrame(tweets)
    df=df[['_id', 'created_at', 'lang', 'place_bounding_box_coordinates',
       'place_country', 'place_country_code', 'place_full_name', 'place_id',
       'place_name', 'place_place_type', 'text', 'user_lang',
       'user_location']]
    df = df.dropna(subset=["place_bounding_box_coordinates"])

    df.text = df.text.apply(prep_txt)

    en = df[df.user_lang == 'en']
    n_en = df[df.user_lang != 'en']

    en_idMap = createMap(en.place_id, en.place_name)
    n_en_idMap = createMap(n_en.place_id, n_en.place_name)

    for k,v in n_en_idMap.items():
        if k not in en_idMap:
            en_idMap[k] = v

    df["place_name_tr"] = df["place_id"].map(en_idMap)

    # calculate bbox centers:
    df["place_center"] = df.place_bounding_box_coordinates.apply(center)

    return df

# db = TweetStore('twitter_locations', COUCH_SERVER)
# tweets = [flatten(dict(t)) for t in db.get_tweets()]
# df = pd.DataFrame(tweets)

# select usefol columns
# df=df[['_id', 'created_at', 'lang', 'place_bounding_box_coordinates',
       # 'place_country', 'place_country_code', 'place_full_name', 'place_id',
       # 'place_name', 'place_place_type', 'text', 'user_lang',
       # 'user_location']]

# drop tweets without location info
# df = df.dropna(subset=["place_bounding_box_coordinates"])

# transform the text data
# df.text = df.text.apply(prep_txt)

# translate place names create 2 maps: one with the id's and place names for the 
# english user i-face data, one for the non-english data. then update the first 
# with the second.
# en = df[df.user_lang == 'en']
# n_en = df[df.user_lang != 'en']

# en_idMap = createMap(en.place_id, en.place_name)
# n_en_idMap = createMap(n_en.place_id, n_en.place_name)

# for k,v in n_en_idMap.items():
#     if k not in en_idMap:
#         en_idMap[k] = v

# df["place_name_tr"] = df["place_id"].map(en_idMap)

# # calculate bbox centers:
# df["place_center"] = df.place_bounding_box_coordinates.apply(center)

df1 = getDF('twitter_belgium_inc', COUCH_SERVER)
df2 = getDF('twitter_locations', COUCH_SERVER)


# write df to csv-file to speed things up
with open("twitter_belgium.csv", 'w') as f1:
    df1.to_csv(f)
with open("twitter_locations.csv", 'w') as f2:
    df2.to_csv(f)
with open("twitter_complete.csv", 'w') as f3:
    df = df1.append(df2)
    df.to_csv(f3)
