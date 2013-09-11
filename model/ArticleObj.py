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

    def del_from_db(self):
        db.session.delete(self)
        db.session.commit()        

    def __repr__(self):
        return '<DbArticle %s>' % self.content
        
class DbQuestion(db.Model):
    '''
    資料庫問題模型
    '''
    __tablename__ = 'QuestionData'
    serial = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, unique=True)
    question = db.Column(db.String(256), unique=True)
    option_a = db.Column(db.String(50), unique=True)
    option_b = db.Column(db.String(50), unique=True)
    option_c = db.Column(db.String(50), unique=True)
    option_d = db.Column(db.String(50), unique=True)
    answer = db.Column(db.Integer, unique=True)
    #options = [option_a, option_b, option_c, option_d]

    def __init__(self, data_array):
        self.article_id = data_array['article_id']
        self.question = data_array['title']
        self.answer = data_array['ans']
        self.option_a = data_array['option_a']
        self.option_b = data_array['option_b']
        self.option_c = data_array['option_c']
        self.option_d = data_array['option_d']

    
    # def __init__(self, article_id, question, answer, *args):
    #     self.article_id = article_id
    #     self.question = question
    #     self.answer = answer
    #     pos = 0
    #     for arg in args:
    #         self.options[pos] = arg
    #         pos = pos + 1
        
    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def del_from_db(self):
        db.session.delete(self)
        db.session.commit()        

    def __repr__(self):
        return '<DbQuestion %s>' % self.content