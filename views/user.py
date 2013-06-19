# -*- coding: utf-8 -*-
"""
    user
    ~~~~~~

    使用者資料、管理的功能部份

"""


from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask import g
from jinja2 import TemplateNotFound

# 資料庫相關
from model.extensions import db
#from model.GameObj import DbGame
from model.UserObj import DbUser
from model.ArticleObj import DbArticle

user = Blueprint('user', __name__)

# @user.before_request
# def before_request():
#     """Make sure we are connected to the database each request and look
#     up the current user so that we know he's there.
#     """
#     #g.db = connect_db()
#     g.user = None
#     if 'user_id' in session:
#         #print "before_request - 111:" + str(session['user_id'])
#         g.user = DbUser.query.filter_by(index=session['user_id']).first()

@user.route('/profile')
@user.route('/profile/<name>')
def profile(name=""):
    '''
    使用者資訊
    '''
    Member_ = g.user
    if name != "":
        Member_ = DbUser.query.filter_by(account=name).first()

    # if g.user == None:
    #     #若不是本人就秀使用者資訊
    #     Member_ = DbUser.query.filter_by(account=name).first()
    #     #articles_ = DbArticle.query.filter_by(member_no=Member_.index)
    #     return render_template('user/Profile.html',Member=Member_)

    #若是本人就秀控制介面
    return render_template('user/Profile.html',Member=Member_)


@user.route('/article')
def article():
    """文章管理介面"""

    # 若沒有登入則轉回首頁
    if g.user == None:
        return redirect( url_for('index') )

    #列出所有文章
    articles_ = DbArticle.query.filter_by(member_no=g.user.index)
    return render_template('user/article.html',Entries=articles_)