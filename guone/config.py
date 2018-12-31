# coding=utf-8

from flask import Flask


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/logindb/login.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'gif', 'tiff', 'bmp', 'jpg', 'JPG'])

YOLO_NAMES = {
    'Chimney': '大烟囱',
    'Apartment': '建大研究生公寓',
    'GongKeBuilding': '建大工科大楼',
    'TennisCourt': '建大网球场',
    'StadiumPodium': '建大体育场主席台'
}
WEIGHT = './darknet detector test cfg/building.data cfg/building_v3.cfg weights/building_v3.weights '
TINY_WEIGHT = './darknet detector test cfg/building.data cfg/building_v3_tiny.cfg weights/building_v3_tiny.weights '
