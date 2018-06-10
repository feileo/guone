# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 17:32:14 2017
@author: atch
"""
import os
import cPickle as pickle

import sift
import imageSearch
from imtools import get_imageList

imlist = get_imageList("../static/data/JianDa1")
imcount = len(imlist)
print imlist
featlist = [imlist[i][:-3] + 'sift' for i in range(imcount)]
print featlist
#imagepkl = r'pickle\vocabulary.pkl'
imagepkl = r"../static\pickle\jianda1.pkl"
with open(imagepkl, 'rb') as f:
    voc = pickle.load(f)

#db = r'db\test.db'
db = r'../static\db\imagedb\jianda1.db'
try:
    os.remove(db)
except OSError:
    pass

idx = imageSearch.Indexer(db, voc)
idx.create_tables()

for i in range(imcount)[:imcount]:
    locs, descr = sift.read_features_from_file(featlist[i])
    idx.add_to_index(imlist[i], descr)

# 提交到数据库
idx.db_commit()
# 检查数据库中的内容
import sqlite3 as sqlite
con = sqlite.connect(db)
print con.execute('select count (filename) from imlist').fetchone()
print con.execute('select * from imlist').fetchone()
