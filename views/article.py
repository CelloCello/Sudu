# -*- coding: utf-8 -*-
"""
    article
    ~~~~~~

    文章管理、發佈相關模組

"""


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask import g, redirect, request, url_for, flash
from model.extensions import db

# 表單
from model.Forms import NewArticleForm
from model.Forms import QuestionForm

# model
from model.ArticleObj import DbArticle
from model.ArticleObj import DbQuestion

article = Blueprint('article', __name__)


# @article.route('/')
# def index():
#     """文章管理介面"""
#     # 若沒有登入則轉回首頁
#     if g.user == None:
#         return redirect( url_for('index') )

#     #列出所有文章
#     articles_ = DbArticle.query.filter_by(member_no=g.user.index)
#     return render_template('user/article.html',Entries=articles_)


#新增文章頁面
@article.route('/new')
def new():
    '''新增文章頁面'''
    form_ = NewArticleForm()
    # for i in xrange(20):
    #     form_.questions.append_entry()
    return render_template('article/new.html', form=form_)


@article.route('/add', methods=['POST'])
def add():
	'''新增文章至資料庫'''
    
    #檢查有無登入
	if g.user == None:
		#沒登入就回到登入頁面
		return redirect(url_for('index'))

	newForm = NewArticleForm()
	if newForm.validate_on_submit():
		newArticle = DbArticle(g.user.index, newForm.content.data, newForm.title.data, newForm.authority.data)
		newArticle.store_to_db()
		flash(u"新增文章成功")
	else:
		flash(u"新增文章失敗")


	return redirect(url_for('user.article'))

@article.route('/edit/<int:serial>')
def edit(serial):
	'''編輯文章'''
    #檢查有無登入
	if g.user == None:
		#沒登入就回到登入頁面
		flash(u"您還沒登入歐~")
		return redirect(url_for('index'))

	article = DbArticle.query.filter_by(index=serial).first()
	if article is None:
		flash(u"沒有這篇文章")
		return redirect(url_for('user.article'))
	aform = NewArticleForm()
	aform.title.data = article.title
	aform.content.data = article.content
	qform = QuestionForm()
	questions = DbQuestion.query.filter_by(article_id=serial)
	print serial	
	return render_template('article/edit.html', article=article, questions=questions
		, form=aform, qform=qform)

@article.route('/edit_over/<int:serial>', methods=['POST'])
def edit_over(serial):
	'''編輯完成'''

    #檢查有無登入
	if g.user == None:
		#沒登入就回到登入頁面
		return redirect(url_for('index'))

	article = DbArticle.query.filter_by(index=serial).first()
	if article is None:
		flash(u"沒有這篇文章")
		return redirect(url_for('user.article'))

	newForm = NewArticleForm()
	if newForm.validate_on_submit():
		article.content = newForm.content.data
		article.title = newForm.title.data
		article.type = newForm.authority.data
		article.modify()
		flash(u"修改文章成功")
	else:
		flash(u"修改文章失敗")


	return redirect(url_for('user.article'))


@article.route('/delete/<int:serial>')
def delete(serial):
	'''刪除文章'''

    #檢查有無登入
	if g.user == None:
		#沒登入就回到登入頁面
		flash(u"您還沒登入歐~")
		return redirect(url_for('index'))

	delArticle = DbArticle.query.filter_by(index=serial).first()

	if delArticle is None:
		flash(u"沒有這篇文章")
		return redirect(url_for('user.article'))

	delArticle.del_from_db()

	flash(u"刪除文章成功")
	return redirect(url_for('user.article'))

@article.route('/add_question', methods=['POST'])
def add_question():
	'''新增問題'''

    #檢查有無登入
	if g.user == None:
		#沒登入就回到登入頁面
		flash(u"您還沒登入歐~")
		return redirect(url_for('index'))

	# 檢查有沒有超過十筆
	all_questions = DbQuestion.query.filter_by(article_id=request.json['article_id'])
	if all_questions.count() >= 20:
		flash(u"已經有二十筆問題了")
		return redirect(url_for('article.edit', serial=request.json['article_id']))

	#print request.json['option_a']
	question = DbQuestion(request.json)
	question.store_to_db()
	#return request.json['title']
	#return str(request.json['article_id'])
	return str(question.serial)

@article.route('/del_question', methods=['POST'])
def del_question():
	'''刪除問題'''

	print "dddddddddddddddddddddddddddddddddd"

    #檢查有無登入
	if g.user == None:
		#沒登入就回到登入頁面
		flash(u"您還沒登入歐~")
		#return redirect(url_for('index'))
		return "ERROR"

	question_id = request.json['index']
	delQuestion = DbQuestion.query.filter_by(serial=question_id).first()
	if delQuestion is None:
		flash(u"沒有這個題目")
		#return redirect(url_for('user.article'))
		return "ERROR"

	# 檢查此文章是你的
	article = DbArticle.query.filter_by(index=delQuestion.article_id).first()
	if article is None:
		flash(u"這個題目沒有相對應的文章")
		return redirect(url_for('user.article'))

	if article.member_no != g.user.index:
		#flash(u"這個題目的文章")
		#return redirect(url_for('user.article'))		
		return "ERROR"

	print "bbbbbbbb"
	delQuestion.del_from_db()

	flash(u"刪除問題成功")
	return "OK"