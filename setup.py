#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from setuptools import find_packages, setup


setup(
    name='guone',
    version='0.0.1',
    license='BSD license',
    author='acthse',
    author_email='acthse@outlook.com',
    url='https://github.com/acthse/guone',
    description='简户外建筑自动识别系统',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=[
        'WTForms',
        'Flask',
        'Flask-Bootstrap',
        'SQLAlchemy',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Werkzeug',
        'pymysql',
        'gevent',
        'scipy',
        'numpy',
        'matplotlib==2.0.2',
        'pandas',
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'guone = guone.app:run',
        ],
    }
)
