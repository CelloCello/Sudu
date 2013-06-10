# -*- coding: utf-8 -*-
"""
    model/GameObj.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    遊戲相關的物件都集中在此

"""

from extensions import db
from datetime import datetime

class DbGame(db.Model):
    '''
    資料庫遊戲模型
    '''
    __tablename__ = 'GameData'
    serial = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    type = db.Column(db.Integer, unique=True)
    author = db.Column(db.Integer, unique=True)
    like = db.Column(db.Integer, unique=True)
    date = db.Column(db.DateTime, unique=False)
    url = db.Column(db.String(256), unique=False)
    
    def __init__(self, name, author, url, type):
        self.name = name
        self.type = type
        self.date = datetime.utcnow()
        self.author = author
        self.like = 0
        self.url = url
        
    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<DbGame %s>' % self.name
        