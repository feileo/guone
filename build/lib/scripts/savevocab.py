# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 17:29:55 2017

@author: atch
"""
import os
import cPickle as pickle
import tic
import sift
import vocabulary
from imtools import get_imageList

imlist = get_imageList("../local/data/JianDa1")
imcount = len(imlist)
print imlist
print imcount
featlist = [imlist[i][:-3] + 'sift' for i in range(imcount)]

tic.k('Start')
for i in range(imcount):
    if not os.path.exists(featlist[i]):
        sift.process_image(imlist[i], featlist[i])
tic.k('sift loaded')

voc = vocabulary.Vocabulary('JianDa1')  # ukbenchtest
voc.train(featlist, k=imcount, subsampling=10)
tic.k('train loaded')

# 保存词汇
#imagepkl = r"pickle\vocabulary.pkl"
imagepkl = r"../static\pickle\jianda1.pkl"
with open(imagepkl, 'wb') as f:
    pickle.dump(voc, f)
print imagepkl, 'is:', voc.name, voc.word_count
