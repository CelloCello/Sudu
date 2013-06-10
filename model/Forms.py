# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, PasswordField, BooleanField,\
     SubmitField, required, RadioField, TextAreaField

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

class NewArticleForm(Form):
    """
    新增文章用的表單
    """
    title = TextField(u"標題", validators=[required()])
    content = TextAreaField(u"內文", validators=[required()])
    authority = RadioField(u"類型", choices=[('value',u'公開'),('value_two',u'私人')])
    submit = SubmitField(u"送出")