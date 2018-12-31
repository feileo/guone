# -*- coding: utf-8 -*-
import cPickle as pickle
import os
import sqlite3 as sqlite

from guone.core import image_search, sift
from guone.core.imtools import get_imageList


imlist = get_imageList("../static/data/JianDa1")
imcount = len(imlist)
featlist = [imlist[i][:-3] + 'sift' for i in range(imcount)]
imagepkl = r"../static\pickle\jianda1.pkl"

with open(imagepkl, 'rb') as f:
    voc = pickle.load(f)

db = r'../static\db\imagedb\jianda1.db'
try:
    os.remove(db)
except OSError:
    pass

idx = image_search.Indexer(db, voc)
idx.create_tables()

for i in range(imcount)[:imcount]:
    locs, descr = sift.read_features_from_file(featlist[i])
    idx.add_to_index(imlist[i], descr)

idx.db_commit()
con = sqlite.connect(db)
print(con.execute('select count (filename) from imlist').fetchone())
print(con.execute('select * from imlist').fetchone())
