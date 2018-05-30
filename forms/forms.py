#-*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, FileField, FormField, BooleanField, StringField, SelectField
from wtforms.validators import Required, EqualTo, DataRequired, Email, Length


class LoginForm(FlaskForm):
    """ 用户登录表单 """
    username = TextField(u"用户名",
                         validators=[Required(message=u'用户名不能为空')],
                         render_kw={'placeholder': u'请输入您设定的用户名', 'class': "form-group form-group-lg"})
    password = PasswordField(u'密码', validators=[Required(message=u'密码不能为空')], render_kw={'placeholder': u'请输入密码'})
    recaptcha = TextField(u'验证码', validators=[Required(message=u'验证码不能为空')], render_kw={'placeholder': u'请输入验证码'})
    Submit = SubmitField(u'现在登录')


class fileForm(FlaskForm):
    """ 图像上传表单 """
    fileupload = FileField(u'',
                           validators=[Required(message=u'您没有选择文件')],
                           render_kw={'class': 'file', 'size': "35", 'style': "width:100px"})
    Submit = SubmitField(u'开始识别', render_kw={'class': 'upload'})


class registerForm(FlaskForm):
    """ 用户注册表单 """
    # email = StringField(u'邮箱', validators=[DataRequired(), Email()], render_kw={'placeholder': u'您的email'})
    username = TextField(u"用户名", validators=[Required(message=u'用户名不能为空')],
                         render_kw={'placeholder': u'设定用户名', 'class': 'control-label'})
    password = PasswordField(u'您的密码',
                             validators=[Required(message=u'密码不能为空'),
                                         EqualTo('confirm', message=u'两次输入密码必须一致!'),
                                         Length(min=6, max=10)], render_kw={'placeholder': u'由6-10个字符或数字组成'})
    confirm = PasswordField(u'再次输入以确认', render_kw={'placeholder': u'两次输入务必一致'})
    recaptcha = TextField(u'验证码', validators=[Required(message=u'验证码不能为空')], render_kw={'placeholder': u'请输入验证码'})
    Submit = SubmitField(u'立即注册')
    accept = BooleanField(u'我同意此<a data-toggle="modal" data-target="#templatemo_modal">服务条款</a> 和 <a href="">隐私条例</a><br>',
                          default='checked', validators=[Required(u'请阅读条例!')])
