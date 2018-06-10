# -*- coding: utf-8 -*-

import os

from shutil import copy
from flask_bootstrap import Bootstrap

from views.views import app


def redb(sourceDir, targetDir):
    copy(sourceDir, targetDir)


bootstrap = Bootstrap(app)


def run():
    try:
        # app.run(port=8004, debug=False)
        os.system('./bin/gunicorn -w 1 -b 0.0.0.0:8004  app:app -k gevent')
    except Exception as err:
        print err
    finally:
        redb(r'static/db/redb/jianda1.pkl', r'static/pickle/jianda1.pkl')
        redb(r'static/db/redb/jianda1.db', r'static/db/imagedb/jianda1.db')


if __name__ == "__main__":
    run()
