# -*- coding: utf-8 -*-

import logging
import os
from shutil import copy

from flask_bootstrap import Bootstrap

from views.views import app


def redb(source_dir, target_dir):
    copy(source_dir, target_dir)


bootstrap = Bootstrap(app)


def run():
    try:
        app.run()
    except Exception as err:
        logging.error(err)
    finally:
        redb('static/db/redb/jianda1.pkl', 'static/pickle/jianda1.pkl')
        redb('static/db/redb/jianda1.db', 'static/db/imagedb/jianda1.db')


if __name__ == "__main__":
    run()
