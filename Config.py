#coding:utf-8

import os

_HERE = os.path.dirname(__file__)
_DB_SQLITE_PATH = os.path.join(_HERE, 'DBInfo.db')

# _DBUSER = "root"  # 数据库用户名
# _DBPASS = "123"  # 数据库用户名密码
# _DBHOST = "localhost"  # 服务器
# _DBNAME = "fblog"  # 数据库名称

class Config(object):
    #SECRET_KEY = '\xb5\xc8\xfb\x18\xba\xc7*\x03\xbe\x91{\xfd\xe0L\x9f\xe3\\\xb3\xb1P\xac\xab\x061'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % _DB_SQLITE_PATH
    SECRET_KEY = 'development key'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    MAX_IMG_SIZE = 256
    #BABEL_DEFAULT_TIMEZONE = 'Asia/Chongqing'
    #MAX_CONTENT_LENGTH = 1 * 1024 * 1024


# class ProConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True

    
