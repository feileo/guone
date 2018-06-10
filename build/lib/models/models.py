# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

from config import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            db.session.rollback()
            print e
        finally:
            return 0

    def isExisted(self):
        temUser = User.query.filter_by(username=self.username).first()
        print temUser
        if temUser is None:
            return 0
        else:
            return 1
