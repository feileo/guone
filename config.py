# coding=utf-8

from flask import Flask
import sqlite3
# import pymysql


app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/test'
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///static/db/logindb/login.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


UPLOAD_FOLDER = r'static/images'
ALLOWED_EXTENSIONS = set(['png', 'gif', 'tiff', 'bmp', 'jpg', 'JPG'])

YOLO_NAMES = {
    'Chimney': u'大烟囱',
    'Apartment': u'建大研究生公寓',
    'GongKeBuilding': u'建大工科大楼',
    'TennisCourt': u'建大网球场',
    'StadiumPodium': u'建大体育场主席台'
}
