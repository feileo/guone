# -*- coding: utf-8 -*-
# flake8: noqa
from setuptools import find_packages, setup


setup(
    name='Guone', version='0.0.1',
    license='PRIVATE',
    author='GuoJiawei',
    author_email='acthse@outlook.com',
    url='',
    description=u'户外建筑自动识别系统',
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
        'pandas',
        'Pillow'  # PIL 改名了
    ],
    entry_points={
        'console_scripts': [
            'Guone = app:run',
        ],
    }
)
