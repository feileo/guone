# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import Required, EqualTo, Length


class LoginForm(FlaskForm):
    """ 用户登录表单 """

    username = TextField(
        "用户名",
        validators=[Required(message='用户名不能为空')],
        render_kw={
            'placeholder': '请输入您设定的用户名',
            'class': "form-group form-group-lg"
        }
    )
    password = PasswordField(
        '密码',
        validators=[Required(message='密码不能为空')],
        render_kw={'placeholder': '请输入密码'}
    )
    recaptcha = TextField(
        '验证码',
        validators=[Required(message='验证码不能为空')],
        render_kw={'placeholder': '请输入验证码'}
    )
    Submit = SubmitField('现在登录')


class FileForm(FlaskForm):
    """ 图像上传表单 """

    fileupload = FileField(
        '',
        validators=[Required(message='您没有选择文件')],
        render_kw={'class': 'file', 'size': "35", 'style': "width:100px"}
    )
    Submit = SubmitField('开始识别', render_kw={'class': 'upload'})


class RegisterForm(FlaskForm):
    """ 用户注册表单 """

    username = TextField(
        "用户名",
        validators=[Required(message='用户名不能为空')],
        render_kw={'placeholder': '设定用户名', 'class': 'control-label'}
    )
    password = PasswordField(
        '您的密码',
        validators=[
            Required(message='密码不能为空'),
            EqualTo('confirm', message='两次输入密码必须一致!'),
            Length(min=6, max=10)
        ],
        render_kw={'placeholder': '由6-10个字符或数字组成'}
    )
    confirm = PasswordField(
        '再次输入以确认',
        render_kw={'placeholder': '两次输入务必一致'}
    )
    recaptcha = TextField(
        '验证码',
        validators=[Required(message='验证码不能为空')],
        render_kw={'placeholder': '请输入验证码'}
    )
    Submit = SubmitField('立即注册')
    accept = BooleanField(
        '我同意此<a data-toggle="modal" data-target="#templatemo_modal">服务条款</a> 和 <a href="">隐私条例</a><br>',
        default='checked',
        validators=[Required('请阅读条例!')]
    )
