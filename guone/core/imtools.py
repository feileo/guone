# -*- coding: utf-8 -*-
import os

import matplotlib as mpl
from PIL import Image


mpl.use('TkAgg')


def get_imageList(path):
    """ 返回一个文件夹中包含的所有图像文件的文件名列表 """
    return [
        os.path.join(path, f) for f in os.listdir(path)
        if (f.endswith('.jpg') or f.endswith('.JPG'))
    ]


def imresize(im, sz):
    """ 使用 PIL 对象重新定义图像数组的大小 """

    pil_im = Image.fromarray(uint8(im))
    return array(pil_im.resize(sz))


def histeq(im, nbr_bins=256):
    """ 对一幅灰度图像进行直方图均衡化 """

    # 计算图像的直方图
    imhist, bins = histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()
    cdf = 255 * cdf / cdf[-1]  # 归一化

    # 使用累积分布函数的线性插值，计算新的像素值
    im2 = interp(im.flatten(), bins[:-1], cdf)
    return im2.reshape(im.shape), cdf


def compute_average(imlist):
    """ 计算图像列表的平均图像 """

    # 打开第一幅图像，将其存储在浮点型数组中
    averageim = array(Image.open(imlist[0]), 'f')
    for imname in imlist[1:]:
        try:
            averageim += array(Image.open(imname))
        except:
            print imname + '...skipped'  # 跳过不能打开的图片
    averageim /= len(imlist)
    # 返回uint8类型的平均图像
    return array(averageim, 'uint8')


def wimlist():
    imlist = get_imageList("../data/JianDa1")
    print len(imlist)
    with open(r'imlist\imlist.txt', 'w') as f:
        for im in imlist:
            f.writelines(im)
            f.writelines('\n')


def rimlist(path):
    imlist = []
    with open(path, 'r') as f:
        for eachline in f:
            imlist.append(eachline[:-1])
    return imlist
