# -*- coding: utf-8 -*-
"""
    model/UserObj.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    使用者相關的物件都集中在此

"""

from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import AnonymousUser, UserMixin
from extensions import db
from datetime import datetime

class DbUser(db.Model):
    '''
    資料庫使用者模型
    '''
    __tablename__ = 'MemberData'
    index = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(10), unique=True)
    authority = db.Column(db.Integer, unique=True)
    date = db.Column(db.DateTime, unique=False)
    scoin = db.Column(db.Integer, unique=False)
    
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.authority = 0
        self.date = datetime.utcnow()
        self.scoin = 0

    def __repr__(self):
        return '<User %r>' % self.account
        
    def store_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def checkPassword(self, password):
        if self.password == password:
            return True
        return False
        
class Anonymous(AnonymousUser):
    '''
    陌生人的資料結構
    '''
    account = u"Guest"

class LoginUser(UserMixin):
    '''
    登入時要檢查cookie/session的使用者資料結構
    '''
    def __init__(self, id, account, active=True):
        self.id = id
        self.account = account
        self.active = active

    def is_active(self):
        return self.active


    
