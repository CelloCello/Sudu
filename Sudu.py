# -*- coding: utf-8 -*-
"""
    Sudu
    ~~~~~~

    可以讓你練習速讀的網頁

"""

# system
#import Image
from PIL import Image
import os
import random
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
from flaskext.markdown import Markdown

# my tool
from ctools.web_func import get_image_type, check2mkdir

# 資料庫相關
#from flask.ext.sqlalchemy import SQLAlchemy
from model.UserObj import DbUser
from model.ArticleObj import DbArticle
from model.extensions import db
from model.extensions import SerializeModel

# 表單
from model.Forms import LoginForm, RegisterForm

# 藍圖
from views import about
from views import game
from views import user
from views import article

DEFAULT_MODULES = (
(about, '/about'),
(game, '/game'),
(user, '/user'),
(article, '/article'),
)


# create our little application :)
app = Flask(__name__)
app.config.from_object('Config.DevConfig')  #設定config
app.config.from_envvar('SUDU_SETTINGS', silent=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBInfo.db'
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
db.init_app(app)
babel = Babel(app)
Markdown(app)

# 註冊藍圖
def setting_modules(app, modules):
    """ 註冊Blueprint """
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix = url_prefix)

setting_modules(app,DEFAULT_MODULES)

    
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
    articles_ = DbArticle.query.limit(5).all()
    users_ = DbUser.query.order_by(DbUser.date).limit(10)
    return render_template('index.html', Articles=articles_, Users=users_)  
    
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
    # 已經有登入的就秀出你的資訊
    if g.user:
        #return redirect(url_for('showUserProfile',username=g.user.account))
        return redirect(url_for('user.article'))
        
    if request.method == 'POST':
        lgForm_ = LoginForm()
        if lgForm_.validate_on_submit():
            #user_ = DbUser.query.filter_by(account=request.form['account']).first()
            user_ = DbUser.query.filter_by(account=lgForm_.account.data).first()
            
            if user_ is None:
                flash(u'沒有這個人!')
                return render_template('index.html')
            
            if user_.checkPassword(lgForm_.password.data) == False:
                flash(u'密碼錯誤!')
                return render_template('index.html')
                
            #flash('You were logged in')
            session['user_id'] = user_.index
            #session['user_name'] = user['ACCOUNT']
            #print ("id:%d, name:%s") % (user['INDEX'],user['ACCOUNT'])
            #return redirect(url_for('showUserProfile',username=user_.account))
            return redirect(url_for('user.article'))
        
    return "<font color='red'>You should go from index page!!</font>"

    
# #新增文章頁面
# @app.route('/newArticle')
# def newArticle():
#     form_ = NewArticleForm()
#     return render_template('NewArticle.html', form=form_)
    
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
        return redirect(url_for('user.article'))

    error = None
    if request.method == 'POST':
        rgForm_ = RegisterForm()
        if rgForm_.validate_on_submit():
            if not rgForm_.account.data:
                error = 'You have to enter a username'
            elif not rgForm_.password.data:
                error = 'You have to enter a password'
            elif rgForm_.password.data != rgForm_.repassword.data:
                error = 'The two passwords do not match'
            else:
                # 先檢查有沒有註冊過
                oldUser_ = DbUser.query.filter_by(account=rgForm_.account.data).first()
                if oldUser_ is None:
                    newUser_ = DbUser(rgForm_.account.data, rgForm_.password.data)
                    db.session.add(newUser_)
                    db.session.commit()
                    check2mkdir("./static/users/"+rgForm_.account.data)
                    #g.user = newUser_
                    session['user_id'] = newUser_.index
                    flash(u"註冊成功!")
                    #return redirect(url_for('showUserProfile',username=request.form['username']))
                    return redirect(url_for('user.article'))
                else:
                    error = "This account has been used!"
    
    flash(error)
    return redirect(url_for('index'))


# #秀出使用者首頁資訊
# @app.route('/users/<username>')
# def showUserProfile(username):
#     '''
#     show the user profile for that user
#     '''

#     if g.user and g.user.account == username:
#         #若是本人就秀控制介面
#         flash(username)
#         flash("you are "+username)

#         #列出所有文章
#         articles_ = DbArticle.query.filter_by(member_no=g.user.index)
#         #return render_template('show_entries.html', entries=entries)
#         return render_template('UserProfile.html',Member=g.user,Entries=articles_)

#     #若不是本人就秀使用者資訊
#     Member_ = DbUser.query.filter_by(account=username).first()
#     #articles_ = DbArticle.query.filter_by(member_no=Member_.index)
#     return render_template('UserProfile.html',Member=Member_)

#取得熱門清單
@app.route('/hotlist', methods=['GET'])
def getHotList():
    '''取得熱門清單'''
    #t = time.time()
    #hots_ = query_db('''select * from [ArticleData] ''')
    articles_ = DbArticle.query.limit(5).all()
    import json
    return json.dumps(SerializeModel(articles_))

@app.route('/LastUserList')
def getLastUserList():
    '''取得新加入的使用者清單'''
    users_ = DbUser.query.limit(10).order_by(DbUser.date)
    if users_:
        import json
        return json.dumps(SerializeModel(users_))        


@app.route('/getHeadImg/<username>')
@app.route('/getHeadImg/<type>/<username>')
def getHeadImg(username,type='L'):
    '''
    取得頭像
    '''
    filename_ = "/head.jpg"
    if type == "s":
        filename_ = "/head_s.jpg"
    imgPath_ = "users/" + username + filename_
    path_ = url_for('static', filename=imgPath_)

    #先確認有沒有圖
    if not os.path.exists("./"+path_):
        path_ = url_for('static', filename='images/NoHead.png')

    rand_ = random.randint(0,1000)
    path_ = path_+"?"+str(rand_)
    return redirect(path_)
    
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
    #return redirect(url_for('showUserProfile',username=Member_.account))
    return redirect(url_for('user.article'))
    #return "ok!!!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
    #app.run()
