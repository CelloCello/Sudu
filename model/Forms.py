# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, PasswordField, BooleanField,\
     SubmitField, required

class LoginForm(Form):
    """
    登錄用的表單
    """
    account = TextField(u"帳號", validators=[required()])
    password = PasswordField(u"密碼", validators=[required()])
    submit = SubmitField(u"登入")
    
class RegisterForm(Form):
    """
    註冊用的表單
    """
    account = TextField(u"帳號", validators=[required()])
    password = PasswordField(u"密碼", validators=[required()])
    repassword = PasswordField(u"確認密碼", validators=[required()])
    submit = SubmitField(u"註冊")
