# -*- coding: utf-8 -*-
import cPickle as pickle

from guone.core import homography
from guone.core import image_search
from guone.core import sift
from guone.core.imtools import get_imageList


imlist = get_imageList("../data/JianDa1")
imcount = len(imlist)
featlist = [imlist[i][:-3] + 'sift' for i in range(imcount)]


def similarity(res):
    distsum, disti = 0.0, []
    for i in range(len(res[:4])):
        disti.append(res[i][0])
        distsum += disti[i]
    return [1 - disti[j] / distsum for j in range(len(res[:4]))]


imagepkl = r"pickle\jianda1.pkl"
with open(imagepkl, 'rb') as f:
    voc = pickle.load(f)
db = r'db\jianda1.db'
searcher = image_search.Searcher(db, voc)

# 查询图像的索引号和返回的搜索结果数目
query_imid = 1
res_count = 30

ress = searcher.query(imlist[1])
print(similarity(ress))
# 常规查询
res = [w[1] for w in searcher.query(imlist[query_imid])[:res_count]]
print('regular results for query %d:' % query_imid, res)


# 载入查询图像的特征
q_locs, q_descr = sift.read_features_from_file(featlist[query_imid])
fp = homography.make_homog(q_locs[:, :2].T)

# 用RANSAC模型拟合单应性
model = homography.RansacModel()

rank = {}
# 载入搜索结果的图像特征
for ndx in res[1:]:
    locs, descr = sift.read_features_from_file(featlist[ndx - 1])  # res is 1-based

    # 获取匹配数
    matches = sift.match(q_descr, descr)
    ind = matches.nonzero()[0]
    ind2 = [int(matches[i]) for i in ind]
    tp = homography.make_homog(locs[:, :2].T)

    # 计算单应性，对内点计数。如果没有足够的匹配数则返回空列表
    try:
        H, inliers = homography.H_from_ransac(fp[:, ind], tp[:, ind2],
                                              model, match_threshold=4)
    except:
        inliers = []
    # 存储内点数
    rank[ndx] = len(inliers)

# 将字典排序，以首先获取最内层的内点数
sorted_rank = sorted(rank.items(), key=lambda t: t[1], reverse=True)
res_geom = [res[0]] + [s[0] for s in sorted_rank]
print('homography results for query %d' % query_imid, res_geom)


print(image_search.compute_ukbench_score(searcher, imlist))

# 显示靠前的搜索结果
image_search.plot_results(searcher, res[:6])
image_search.plot_results(searcher, res_geom[:6])
