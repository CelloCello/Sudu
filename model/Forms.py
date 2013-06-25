# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, PasswordField, BooleanField,\
     SubmitField, required, RadioField, TextAreaField, FieldList

from flask.ext.wtf import FormField

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

class QuestionForm(Form):
    """問題表單"""
    questions = TextAreaField(u"問題", validators=[required()])
    option_a = TextField(u"選項A", validators=[required()])
    option_b = TextField(u"選項B", validators=[required()])
    option_c = TextField(u"選項C", validators=[required()])
    option_d = TextField(u"選項D", validators=[required()])
    ans = TextField(u"答案", validators=[required()])

    # def __init__(self, *args, **kwargs):
    #     kwargs['csrf_enabled'] = False
    #     super(QuestionForm, self).__init__(*args, **kwargs)


class NewArticleForm(Form):
    """
    新增文章用的表單
    """
    title = TextField(u"標題", validators=[required()])
    content = TextAreaField(u"內文", validators=[required()])
    authority = RadioField(u"類型", choices=[('value',u'公開'),('value_two',u'私人')])
    question = FormField(QuestionForm)
    #questions = FieldList(TextAreaField())
    questions = FieldList(FormField(QuestionForm))
    # questions = content
    # for i in xrange(20):
    #     qu = TextField(u"問題"+str(i), validators=[required()])
    #     questions.append(content)
    #     #questions.append_entry()
    submit = SubmitField(u"送出")

