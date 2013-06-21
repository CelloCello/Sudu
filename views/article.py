# -*- coding: utf-8 -*-
"""
    article
    ~~~~~~

    文章管理、發佈相關模組

"""


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# 表單
from model.Forms import NewArticleForm
from model.Forms import QuestionForm

article = Blueprint('article', __name__)


#新增文章頁面
@article.route('/new')
def new():
    '''新增文章頁面'''
    form_ = NewArticleForm()
    # for i in xrange(20):
    #     form_.questions.append_entry()
    return render_template('article/new.html', form=form_)

@article.route('/site')
def site():
    return render_template('about/site.html')