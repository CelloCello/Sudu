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

user = Blueprint('user', __name__)

@user.route('/profile')
@user.route('/profile/<name>')
def profile(name=""):
    '''
    使用者資訊
    '''

    if g.user == None:
        #若不是本人就秀使用者資訊
        Member_ = DbUser.query.filter_by(account=name).first()
        #articles_ = DbArticle.query.filter_by(member_no=Member_.index)
        return render_template('user/Profile.html',Member=Member_)

    #若是本人就秀控制介面
    return render_template('user/Profile.html',Member=g.user)


