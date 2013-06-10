# -*- coding: utf-8 -*-
"""
    Sudu
    ~~~~~~

    可以讓你練習速讀的網頁

"""

# system
import Image
import os
#import time, datetime
#from __future__ import with_statement
#from sqlite3 import dbapi2 as sqlite3
#from contextlib import closing

# flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, abort
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
#from flask import send_from_directory
from flaskext.babel import Babel

# my tool
from ctools.web_func import get_image_type, check2mkdir

# 資料庫相關
#from flask.ext.sqlalchemy import SQLAlchemy
from model.UserObj import DbUser
from model.ArticleObj import DbArticle
from model.extensions import db
from model.extensions import SerializeModel

# 表單
from model.Forms import LoginForm, RegisterForm, NewArticleForm

# 藍圖
from views import about
from views import game

DEFAULT_MODULES = (
(about, '/about'),
(game, '/game'),
)


# create our little application :)
app = Flask(__name__)
app.config.from_object('Config.DevConfig')  #設定config
app.config.from_envvar('SUDU_SETTINGS', silent=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBInfo.db'
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
db.init_app(app)
babel = Babel(app)

# 註冊藍圖
def setting_modules(app, modules):
    """ 註冊Blueprint """
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix = url_prefix)

setting_modules(app,DEFAULT_MODULES)

# #資料庫查詢
# def query_db(query, args=(), one=False):
#     """Queries the database and returns a list of dictionaries."""
#     return None
    
# def connect_db():
#     """Returns a new connection to the database."""
#     return db
#     #return sqlite3.connect(app.config['DATABASE'])
    
# 檢查上傳檔案是否是可用的副檔
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
@app.before_request
def before_request():
    """Make sure we are connected to the database each request and look
    up the current user so that we know he's there.
    """
    #g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        #print "before_request - 111:" + str(session['user_id'])
        g.user = DbUser.query.filter_by(index=session['user_id']).first()


# @app.teardown_request
# def teardown_request(exception):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'db'):
#         g.db.close()

    
#速讀頁面
@app.route('/sudu/<int:ID>')
def sudu(ID):
    '''
    速讀主頁面
    '''
    
    #檢查有無登入
    if g.user == None:
        #沒登入就回到登入頁面
        return redirect(url_for('index'))
        
    #找出文章
    #Article_ = query_db("select TITLE, ARTICLE from ArticleData where [INDEX]=?",[ID],one=True)
    Article_ = DbArticle.query.filter_by(index=ID).first()
    if Article_ is None:
        return u"<font color='red'>沒有這篇文章!!!</font>"
        
    return render_template('sudu/sudu.html',Text=Article_)

#首頁
@app.route('/')
def index():
    flash(u'你進到首頁了!!')        
    return render_template('index.html')
    
# #Login頁面(目前用不到)
# @app.route('/login', methods=['GET'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html',Type=request.args.get('type'))
#     else:
#         return render_template('login.html',Type="reg")

#Login檢查頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    print "you login!!!"
    # 已經有登入的就秀出你的資訊
    if g.user:
        return redirect(url_for('showUserProfile',username=g.user.account))
        
    error = None
    if request.method == 'POST':
        user_ = DbUser.query.filter_by(account=request.form['account']).first()
            
        if user_ is None:
            flash(u'沒有這個人!')
            return render_template('index.html')
        
        if user_.checkPassword(request.form['password']) == False:
            flash(u'密碼錯誤!')
            return render_template('index.html')
            
        flash('You were logged in')
        session['user_id'] = user_.index
        #session['user_name'] = user['ACCOUNT']
        #print ("id:%d, name:%s") % (user['INDEX'],user['ACCOUNT'])
        return redirect(url_for('showUserProfile',username=user_.account))
        
    return "<font color='red'>You should go from index page!!</font>"

    
#新增文章頁面
@app.route('/newArticle')
def newArticle():
    form_ = NewArticleForm()
    return render_template('NewArticle.html', form=form_)
    
#登出
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))

#取得註冊介面
@app.route('/getSignup')
def getSignup():
    form_ = RegisterForm()
    return render_template('register.html', form=form_, type="Signup")
    
#取得登入介面
@app.route('/getSignin')
def getSignin():
    form_ = LoginForm()
    return render_template('register.html', form=form_, type="Signin")
    
#使用者註冊介面
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""    
    if g.user:
        Member_ = query_db('''select * from MemberData where [INDEX] = ?''',
        [session['user_id']], one=True)
        return redirect(url_for('showUserProfile',username=Member_['ACCOUNT']))
        
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        #elif not request.form['email'] or \
        #         '@' not in request.form['email']:
        #    error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        #elif get_user_id(request.form['username']) is not None:
        #    error = 'The username is already taken'
        else:
            NewUser_ = User(request.form['username'],request.form['password'])
            db.session.add(NewUser_)
            db.session.commit()
            check2mkdir("./static/users/"+request.form['username'])
            flash(u"註冊成功!")
            return redirect(url_for('showUserProfile',username=request.form['username']))
      
    flash(error)
    return redirect(url_for('index'))


#秀出使用者首頁資訊
@app.route('/user/<username>')
def showUserProfile(username):
    '''
    show the user profile for that user
    '''

    if g.user and g.user.account == username:
        #若是本人就秀控制介面
        flash(username)
        flash("you are "+username)

        #列出所有文章
        articles_ = DbArticle.query.filter_by(member_no=g.user.index)
        #return render_template('show_entries.html', entries=entries)
        return render_template('UserProfile.html',Member=g.user,Entries=articles_)

    #若不是本人就秀使用者資訊
    Member_ = DbUser.query.filter_by(account=username).first()
    #articles_ = DbArticle.query.filter_by(member_no=Member_.index)
    return render_template('UserProfile.html',Member=Member_)

#取得熱門清單
@app.route('/hotlist', methods=['GET'])
def getHotList():
    #t = time.time()
    #hots_ = query_db('''select * from [ArticleData] ''')
    articles_ = DbArticle.query.limit(5).all()
    import json
    return json.dumps(SerializeModel(articles_))
    
@app.route('/upImg',methods=['GET', 'POST'])
def upImg():
    #print "upImg"
    #要登入才能上傳
    if g.user:       
        error = None
        # Member_ = query_db('''select * from MemberData where [INDEX] = ?''',
        #     [session['user_id']], one=True)
        Member_ = g.user

        #print request.form['imgfile']
        if request.method == 'POST':
            # try:
                # self.file_ = request.files['file']
            # except RequestEntityTooLarge, e:
                # flash(u"too large")
                # print "aaa"
                # return redirect(url_for('showUserProfile',username=Member_['ACCOUNT']))
                
            #print "post"
            file_ = request.files['file']
            if not file_ or not allowed_file(file_.filename):
                error = 'You have to enter a file'
                #print "no file"
            else:
                #print "request"
                file_ = request.files['file']
                #parser_ = ImageFile.Parser()
                #for chunk_ in file_.chunks():
                #    parser_.feed(chunk)
                #img_ = parser_.close()
                #img_.save("//aaa.jpg","JPGE")
                # if get_image_type(file_.read(), is_path=False) is None:
                    # errors = u'目前圖片僅支援jpg,png,bmp,gif!'
                    # return "NG!"

                #圖片轉型 and 縮圖
                print "file allow"
                #imgData_ = file_.read()
                img_ = Image.open(file_)
                imgSizeX_ = img_.size[0]
                imgSizeY_ = img_.size[1]
                if imgSizeY_ > app.config['MAX_IMG_SIZE']:
                    newY_ = app.config['MAX_IMG_SIZE']
                    rate_ = float(imgSizeY_) / app.config['MAX_IMG_SIZE']
                    #print "orgsize:" + str(imgSizeX_) + ", " + str(imgSizeY_) + ", " + str(rate_)
                    newX_ = imgSizeX_ / rate_
                    #print "newsize:" + str(newX_) + ", " + str(newY_) + ", " + str(rate_)
                    img_ = img_.resize( (int(round(newX_)),int(round(newY_))) )
                imgS_ = img_.resize( (36,36) )
                # fNames_ = os.path.splitext(file_.filename)
                # out_ = file(".//static//users//"+Member_['ACCOUNT']+"//Head"+fNames_[-1], "w")
                # outS_ = file(".//static//users//"+Member_['ACCOUNT']+"//Head_s"+fNames_[-1], "w")
                # img_.save(out_,"JPEG")
                # img_.save(outS_,"JPEG")
                img_.save(".//static//users//"+Member_.account+"//Head.jpg","JPEG")
                imgS_.save(".//static//users//"+Member_.account+"//Head_s.jpg","JPEG")
                #file_.save(".//static//users//"+Member_['ACCOUNT']+"//Head"+fNames_[-1])
                filename_ = secure_filename(file_.filename)
                flash(u"上傳結束00",'error')
                return redirect(url_for('upImg',filename=filename_))
      
    #flash(u"NG")
    #print "upImg end"
    return redirect(url_for('showUserProfile',username=Member_.account))
    #return "ok!!!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    #app.run()
