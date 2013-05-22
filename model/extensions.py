#coding:utf-8

#from flaskext.sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
#from flaskext.script import Manager
import datetime

db = SQLAlchemy()
#manager = Manager()

# 將SQLAlchemy的物件轉成Dict
def Obj2Dict(obj):
    result = {}
    for key in obj.__mapper__.c.keys():
        data = getattr(obj, key)

	try:
		if isinstance(data, datetime.datetime):
			data = data.strftime('%Y-%m-%d %H:%M:%S')
		#json.dumps(data) # this will fail on non-encodable values, like other classes  
		result[key] = data  
	except TypeError:
		result[key] = None  

    return result

# 將SQLAlchemy查到的結果轉成json可以dump的格式
def SerializeModel(model):
	serialized_ = [
		Obj2Dict(data)
		for data in model
	]
	return serialized_
