# -*- coding: utf-8 -*-
"""
    Sudu
    ~~~~~~

    可以讓你練習速讀的網頁

"""


#from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
#from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, abort

from ctools.web_func import get_image_type, check2mkdir
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import send_from_directory
     
import Image
import os
     
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
DATABASE = 'DBInfo.db'
DEBUG = True
SECRET_KEY = 'development key'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('SUDU_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DBInfo.db'
#app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

db = SQLAlchemy(app)

#定義資料庫使用者類別
class User(db.Model):
    __tablename__ = 'MemberData'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(10), unique=True)
    authority = db.Column(db.Integer, unique=True)
    
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.authority = 0

    def __repr__(self):
        return '<User %r>' % self.account

#資料庫查詢
def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    #print "==========="
    #print args
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv
    
def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])
    
# 檢查上傳檔案是否是可用的副檔
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
@app.before_request
def before_request():
    """Make sure we are connected to the database each request and look
    up the current user so that we know he's there.
    """
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('''select * from MemberData where [INDEX] = ?''',
        [session['user_id']], one=True)


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

	
#速讀網
@app.route('/sudu/<int:ID>')
def sudu(ID):
    
    #檢查有無登入
    if g.user == None:
        #沒登入就回到登入頁面
        return redirect(url_for('index'))
        
    #找出文章
    Article_ = query_db("select TITLE, ARTICLE from ArticleData where [INDEX]=?",[ID],one=True)
    if Article_ is None:
        return u"<font color='red'>沒有這篇文章!!!</font>"
        
    return render_template('sudu.html',Text=Article_)

#首頁
@app.route('/')
def index():
    #flash(u'你進到首頁了!!')
    if g.user:
        #flash(session['user_id'])
        Member_ = query_db('''select * from MemberData where [INDEX] = ?''',
        [session['user_id']], one=True)
        #print("aaaa")
        #print(Member_['ACCOUNT'])
        return redirect(url_for('show_user_profile',username=Member_['ACCOUNT']))
        
    return render_template('index.html')
    
#Login頁面(目前用不到)
@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html',Type=request.args.get('type'))
    else:
        return render_template('login.html',Type="reg")

#Login檢查頁面
@app.route('/loginCheck', methods=['GET', 'POST'])
def loginCheck():
    """Logs the user in."""
    
    if g.user:
        Member_ = query_db('''select * from MemberData where [INDEX] = ?''',
        [session['user_id']], one=True)
        return redirect(url_for('show_user_profile',username=Member_['ACCOUNT']))
        
    error = None
    if request.method == 'POST':
        #print request.form['username']
        user = query_db('''select * from MemberData where
            ACCOUNT = ?''', [request.form['username']], one=True)
            
        if user is None:
            flash(u'沒有這個人!')
            return render_template('index.html')
        
        if user['PASSWORD'] != request.form['password']:
            flash(u'密碼錯誤!')
            return render_template('index.html')
            
        flash('You were logged in')
        session['user_id'] = user['INDEX']
        #session['user_name'] = user['ACCOUNT']
        #print ("id:%d, name:%s") % (user['INDEX'],user['ACCOUNT'])
        #return render_template('index.html')
        return redirect(url_for('show_user_profile',username=user['ACCOUNT']))
        
    return "<font color='red'>You should go from index page!!</font>"
        # if user is None:
            # error = 'Invalid username'
        # elif not check_password_hash(user['pw_hash'],
                                     # request.form['password']):
            # error = 'Invalid password'
        # else:
            # flash('You were logged in')
            # session['user_id'] = user['INDEX']
            # session['user_name'] = user['ACCOUNT']
            # print ("id:%d, name:%s") % (user['INDEX'],user['ACCOUNT'])
            #return redirect(url_for('timeline'))
    #return render_template('login.html', error=error)
    
#新增文章頁面
@app.route('/newArticle')
def newArticle():
    return render_template('NewArticle.html')
    
#登出
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))
    
#使用者註冊介面
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""    
    if g.user:
        Member_ = query_db('''select * from MemberData where [INDEX] = ?''',
        [session['user_id']], one=True)
        return redirect(url_for('show_user_profile',username=Member_['ACCOUNT']))
        
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
            return redirect(url_for('show_user_profile',username=request.form['username']))
      
    flash(error)
    return redirect(url_for('index'))
    
#取得大頭貼(測試用,目前沒用到)
def getHeadImg1(username):
    Path_ = "./static/users/" + username + "/head.jpg"
    #先確認有沒有圖
    if not os.path.exists(Path_):
        Path_ = "./static/images/NoHead.png"
    return Path_
    
#取得大頭貼(測試用,目前沒用到)
@app.route('/img/head2/<username>', methods=['GET'])
def getHeadImg2(username):
    print "aaaaa"
    Path_ = "./static/users/" + username + "/head.jpg"
    #if request.method == 'GET':
    #先確認有沒有圖
    print "bbbb"
    if not os.path.exists(Path_):
        Path_ = "./static/images/NoHead.png"

    print Path_
    return Path_
    
#取得大頭貼
@app.route('/img/head/<username>')
def getHeadImg(username):
    flash("getHead")
    print "getHead"
    Path_ = "./static/users/" + username + "/head.jpg"
    # Path_ = "./static/users/" + username
    # ImgName_ = "/Head"
    # Full_ = Path_ + ImgName_
    #先確認有沒有圖
    if not os.path.exists(Path_):
        Path_ = "./static/images/NoHead.png"
        # Path_ = "./static/images"
        # ImgName_ = "/NoHead"

    # ExtName_ = get_image_type("./static/images"+ImgName_) 
    # Path_ = Path_ + ImgName_ + "." + ExtName_
    # Path_ = Path_ + ImgName_ + "." + ExtName_
    # print Path_
    imgPath_ = "<img src='%s' height='42' width='42'/>" % Path_
    import random
    rand_ = random.randint(0,1000)
    print Path_+"?"+str(rand_)
    return redirect(Path_+"?"+str(rand_))


#秀出使用者首頁資訊
@app.route('/<username>')
def show_user_profile(username):
    # show the user profile for that user
    Member_ = query_db('''select * from MemberData where [ACCOUNT] = ?''',
        [username], one=True)
    if Member_ is None:
        abort(404)
		
    #HeadImgPath_ = getHeadImg1(username)
    #print HeadImgPath_
    if g.user and g.user['ACCOUNT'] == username:
        #若是本人就秀控制介面
        flash(username)
        flash("you are "+username)
        
        #列出所有文章
        entries = query_db('''select * from ArticleData where [MEMBER_NO]=?''',
            [Member_['INDEX']])
        #return render_template('show_entries.html', entries=entries)
        return render_template('UserProfile.html',Member=Member_,Entries=entries)

    #若不是本人就秀使用者資訊
    return render_template('UserProfile.html',Member=Member_)
	#return "you are "+username
    
@app.route('/upImg',methods=['GET', 'POST'])
def upImg():
    #print "upImg"
    #要登入才能上傳
    if g.user:       
        error = None
        Member_ = query_db('''select * from MemberData where [INDEX] = ?''',
            [session['user_id']], one=True)

        #print request.form['imgfile']
        if request.method == 'POST':
            # try:
                # self.file_ = request.files['file']
            # except RequestEntityTooLarge, e:
                # flash(u"too large")
                # print "aaa"
                # return redirect(url_for('show_user_profile',username=Member_['ACCOUNT']))
                
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
                img_ = Image.open(file_).resize( (126,126) )
                imgS_ = img_.resize( (42,42) )
                # fNames_ = os.path.splitext(file_.filename)
                # out_ = file(".//static//users//"+Member_['ACCOUNT']+"//Head"+fNames_[-1], "w")
                # outS_ = file(".//static//users//"+Member_['ACCOUNT']+"//Head_s"+fNames_[-1], "w")
                # img_.save(out_,"JPEG")
                # img_.save(outS_,"JPEG")
                img_.save(".//static//users//"+Member_['ACCOUNT']+"//Head.jpg","JPEG")
                imgS_.save(".//static//users//"+Member_['ACCOUNT']+"//Head_s.jpg","JPEG")
                #file_.save(".//static//users//"+Member_['ACCOUNT']+"//Head"+fNames_[-1])
                filename_ = secure_filename(file_.filename)
                flash(u"上傳結束00",'error')
                return redirect(url_for('upImg',filename=filename_))
      
    #flash(u"NG")
    #print "upImg end"
    return redirect(url_for('show_user_profile',username=Member_['ACCOUNT']))
    #return "ok!!!"

if __name__ == '__main__':
    app.debug = True
    #app.run(host='0.0.0.0')
    app.run()
