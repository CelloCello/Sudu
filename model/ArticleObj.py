# -*- coding: utf-8 -*-
"""
    model/ArticleObj.py
    ~~~~~~~~~~~~~~~~~~~~~~~~

    文章相關的物件都集中在此

"""

from extensions import db
from datetime import datetime

class DbArticle(db.Model):
    '''
    資料庫文章模型
    '''
    __tablename__ = 'ArticleData'
    index = db.Column(db.Integer, primary_key=True)
    member_no = db.Column(db.Integer, unique=True)
    content = db.Column(db.Text, unique=True)
    title = db.Column(db.String(20), unique=True)
    type = db.Column(db.Integer, unique=True)
    #img_name = db.Column(db.String(25), unique=False)
    date = db.Column(db.DateTime, unique=False)
    #author = db.Column(db.String(15), unique=False)
    
    def __init__(self, member_no, content, title, type):
        #self.index = index
        self.member_no = member_no
        self.content = content
        self.title = title
        self.type = type
        #self.img_name = img_name
        self.date = datetime.utcnow()
        #self.author = author
        
    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<DbArticle %s>' % self.content
        