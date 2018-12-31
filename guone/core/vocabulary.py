# -*- coding: utf-8 -*-
import numpy
from numpy import *
from scipy.cluster.vq import *
from scripts import sift


class Vocabulary(object):

    def __init__(self, name):
        self.name = name
        self.voc = []
        self.idf = []
        self.trainingdata = []
        self.word_count = 0

    def train1(self, featurefiles, k=100, subsampling=10):
        """ 用含有K个单词的K-means列出在featurefiles中的特征文件训练出一个词汇。
            对训练数据下采样可以加快训练速度"""

        nbr_images = len(featurefiles)
        # 从文件中读取特征
        descr = []
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0]  # 将所有的特征并在一起，以便后面进行k-means聚类
        for i in arange(1, nbr_images):
            descr.append(sift.read_features_from_file(featurefiles[i])[1])
            descriptors = vstack((descriptors, descr[i]))

        # k-means: 最后一个参数决定运行次数
        self.voc, distortion = kmeans(descriptors[::subsampling, :], k, 1)
        self.nbr_words = self.voc.shape[0]

        # 遍历所有图像的训练图像，并投影到词汇上
        imwords = zeros((nbr_images, self.nbr_words))
        for i in range(nbr_images):
            imwords[i] = self.project(descr[i])

        nbr_occurences = sum((imwords > 0) * 1, axis=0)

        self.idf = log((1.0 * nbr_images) / (1.0 * nbr_occurences + 1))
        self.trainingdata = featurefiles

    def train(self, featurefiles, k=100, subsampling=10):
        """ 用含有K个单词的K-means列出在featurefiles中的特征文件训练出一个词汇。
            对训练数据下采样可以加快训练速度 """

        image_count = len(featurefiles)

        descr = []
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0]  # Stack features for k-means.
        for i in numpy.arange(1, image_count):
            descr.append(sift.read_features_from_file(featurefiles[i])[1])
            descriptors = numpy.vstack((descriptors, descr[i]))

        # Run k-means.
        self.voc, distortion = kmeans(descriptors[::subsampling, :], k, 1)
        self.word_count = self.voc.shape[0]

        # 关于词汇的项目培训数据。
        imwords = numpy.zeros((image_count, self.word_count))
        for i in range(image_count):
            imwords[i] = self.project(descr[i])

        occurence_count = numpy.sum((imwords > 0) * 1, axis=0)

        self.idf = numpy.log(image_count / (occurence_count + 1.0))
        self.trainingdata = featurefiles

    def project1(self, descriptors):
        """ 将描述子投影到词汇上，以创建单词直方图 """

        # 图像单词直方图
        imhist = zeros((self.nbr_words))
        words, distance = vq(descriptors, self.voc)
        for w in words:
            imhist[w] += 1

        return imhist

    def project(self, descriptors):
        """词汇表项目描述符，用于创建单词直方图。"""

        imhist = numpy.zeros((self.word_count))
        words, distance = vq(descriptors, self.voc)
        for w in words:
            imhist[w] += 1

        return imhist

    def get_words(self, descriptors):
        """ 将描述符转换为单词。 """

        return vq(descriptors, self.voc)[0]
