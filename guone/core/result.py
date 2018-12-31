# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cPickle as pickle
import os

from PIL import Image

from guone.core import sift, vocabulary


def similarity(res):
    """计算相似度
    Arguments:
            res：图像索引
    """
    distsum, disti = 0.0, []
    for i in range(len(res[:4])):
        disti.append(res[i][0])
        distsum += disti[i]
    return [1 - disti[j] / distsum for j in range(len(res[:4]))]

# def savefile(filepath):
# 	"""将上传图片设置成640*480像素，并以jpg格式保存至原文件夹
# 	[description]
# 	Arguments:
# 		@filepath:用户上传文件的保存路径
# 	Returns:
#     	文件路径
# 	"""
# 	outimage = [os.path.splitext(filepath)[0] + ".jpg"]
# 	if filepath != outimage[0]:
# 		try:
# 			ima = Image.open(filepath)
# 			ima.thumbnail((640,480))
# 			ima.save(outimage[0])
# 		except IOError,e:
# 			print e
# 	return outimage


def buildindex(filepath):
    """完成对加载图像的单词训练以及向数据库添加索引
    Arguments:
            @outimage:文件路径
    Returns:
    待识别文件名
    """
    outimage = [os.path.splitext(filepath)[0] + ".jpg"]
    if filepath != outimage[0]:
        try:
            ima = Image.open(filepath)
            ima.thumbnail((640, 480))
            ima.save(outimage[0])
        except IOError, e:
            print e
    featlist = [outimage[0][:-3] + 'sift']
    sift.process_image(outimage[0], featlist[0])
    # 训练该图像
    upvoc = vocabulary.Vocabulary(os.path.basename(outimage[0]))
    upvoc.train(featlist, k=1, subsampling=10)
    imagename, suffix = os.path.basename(filepath).split('.', 1)
    # 保存该图像词汇
    imagespkl = r"static/pickle/jianda1.pkl"
    with open(imagespkl, 'ab') as f:
        pickle.dump(upvoc, f)
    with open(imagespkl, 'rb') as f:
        voc = pickle.load(f)

    db = 'static/db/imagedb/jianda1.db'
    idx = image_search.Indexer(db, voc)
    # 载入查询图像的特征
    locs, descr = sift.read_features_from_file(featlist[0])
    # 将新图像添加到数据库
    idx.add_to_index(outimage[0], descr)
    # 提交到数据库
    idx.db_commit()
    return outimage[0]


def queryresults(imageurl=None):
    """完成对图像的查询,并返回查询结果html(str)
    Keyword Arguments:
            @imageurl:待查图像URL
    Returns:
    结果str
    """
    imagespkl = r"static/pickle/jianda1.pkl"
    with open(imagespkl, 'rb') as f:
        voc = pickle.load(f)
    maxresults = 38
    req, i = 0, 0
    rehtml = '<h4><br><br>'
    db = r'static/db/imagedb/jianda1.db'
    searcher = image_search.Searcher(db, voc)
    if imageurl:
        # 查询数据库并获取靠前的图像
        res = searcher.query(imageurl)[:maxresults]
        simi = similarity(res)
        for dist, ndx in res:
            imname = searcher.get_filename(ndx)
            if 0 == req:
                pass
            if 0 == i:
                if req in [1, 2, 3, 4]:
                    rehtml += '<img src="/static/data/%s" width=145>' % os.path.basename(imname)
                    rehtml += '&emsp;'
                    rehtml = rehtml + \
                        '<font color="" size="2">相似度: '.decode(
                            "utf-8") + u'%.1f' % float(simi[req - 1] * 100)  # Similarity
                    rehtml += u'%</font>&emsp;&emsp;&emsp;'
                    if 1 == req:
                        bestimagename, suffix = os.path.basename(imname).split('.', 1)[0].split('-')
                        bestimagename = bestimagename.split("\\")[1]
                    elif 4 == req:
                        rehtml += '</h4>'
                        rehtml += '<hr>'
                        rehtml += '<h4><font color="">对该图像的最佳猜测为：&emsp;%s</font></h4>'.decode(
                            "utf-8") % getchname(bestimagename).decode('gbk').encode('utf-8').decode('utf-8')
            req += 1
        return rehtml


def getchname(imageenname):
    """返回图像中文名
    Arguments:
            @imageenname：图像英文名
    """
    with open(r'static/data/namedict.txt', 'r') as f:
        for eachline in f:
            enname, chname = eachline.split(':')
            if imageenname == enname:
                return chname
        else:
            return u'系统未能识别.'
