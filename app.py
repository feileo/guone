# -*- coding: utf-8 -*-

import os

from shutil import copy
from flask_bootstrap import Bootstrap

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from views.views import app


def redb(sourceDir, targetDir):
    copy(sourceDir, targetDir)


app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)

# 启动服务
if __name__ == "__main__":
    try:
        app.run(port=8004, debug=True)
    except Exception as err:
        print err
    finally:
        redb(r'static/db/redb/jianda1.pkl', r'static/pickle/jianda1.pkl')
        redb(r'static/db/redb/jianda1.db', r'static/db/imagedb/jianda1.db')
