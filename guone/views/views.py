# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import StringIO
import os
import time
from guone.config import (
    ALLOWED_EXTENSIONS, YOLO_NAMES, UPLOAD_FOLDER,
    WEIGHT as WEIGHT_CMD, TINY_WEIGHT as TINY_WEIGHT_CMD
)

from flask import (
    flash, url_for, current_app, render_template,
    request, redirect, session
)
from werkzeug import secure_filename

from guone.core import result
from guone.core.verifycode import ImageChar
from guone.forms.forms import RegisterForm, LoginForm, FileForm
from guone.models.models import User, app


app.config['SECRET_KEY'] = '\xf0\xd6n\xd7\xbfO\x10\x0bg\x9c\xc2L]~\x9e<r\xc3\xa6r\xf6U\xd4\xdd'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

COMPLEX_MODE = '21'
SIMPLE_MODE ='22'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_cr(output_info):
    out = []
    for each_line in output_info:
        if any(
            [
                o in each_line for o in [
                    'Chimney', 'Apartment', 'GongKeBuinding', 'TennisCourt', 'StadiumPodium'
                ]
            ]
        ):
            out.append(each_line)
    names, cvs = [], []
    for each_out in out:
        names.append(
            YOLO_NAMES.get(each_out.split(':')[0].strip()) + ' ( {} )'.format(
                each_out.split(':')[0].strip())
        )
        cvs.append(each_out.split(':')[1])
    return names, cvs


@app.route('/code', methods=['GET'])
def generate_code():
    ic = ImageChar(fontColor=(100, 211, 90))
    strs, code_img = ic.randChinese(5)
    session['recaptcha'] = strs
    buf = StringIO.StringIO()
    code_img.save(buf, 'PNG', quality=70)
    buf_str = buf.getvalue()
    response = current_app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/PNG'
    return response


@app.route("/", methods=['GET', 'POST'])
def index():
    myForm = LoginForm()
    if myForm.validate_on_submit():
        if session['recaptcha'].lower() == myForm.recaptcha.data.lower():
            user = User(myForm.username.data, myForm.password.data)
            session['username'] = myForm.username.data
            if (user.isExisted()):
                return redirect(url_for('home'))
            else:
                flash('出错啦,登录失败,请检查用户名和密码是否正确!')
        else:
            flash('Hi, 验证码错误, 请重输!')
    return render_template('index.html', form=myForm)


@app.route("/register", methods=['GET', 'POST'])
def register():
    regForm = RegisterForm()
    if regForm.validate_on_submit():
        if session['recaptcha'].lower() == regForm.recaptcha.data.lower():
            session['username'] = regForm.username.data
            query_obj = User(regForm.username.data, regForm.password.data)
            if(query_obj.isExisted()):
                flash('此用户名已经被使用，请重新注册!')
                del query_obj
                return render_template('register.html', form=regForm)
            else:
                user = User(regForm.username.data, regForm.password.data)
                user.add()
                flash('恭喜您,注册成功,您现在可以登录!')
                return redirect(url_for('index'))
        else:
            flash('Hi, 验证码错误, 请重输!')
    return render_template('register.html', form=regForm)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('username'):
        flash('请您先登录系统!')
        return redirect(url_for('index'))
    return render_template('home.html')


@app.route('/example', methods=['GET', 'POST'])
def example():
    if not session.get('username'):
        flash('请您先登录系统!')
        return redirect(url_for('index'))
    return render_template('video.html')


@app.route('/intro', methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')


@app.route('/upload/<mode>', methods=['GET', 'POST'])
def upload(mode):
    myfileForm = FileForm(request.form)
    if not session.get('username'):
        flash('请您登录系统!')
        return redirect(url_for('index'))
    if request.method == 'POST':
        file = request.files['fileupload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(
                url_for('predicted', mode=mode, filename=filename)
            )
        else:
            flash("出错啦,暂不支持格式此图像文件,请您重新选择文件")
    return render_template('input.html', form=myfileForm, mode=mode, str=str)


@app.route('/predicted/<mode>/<filename>', methods=['GET', 'POST'])
def predicted(mode, filename):
    if mode == str(1):
        filepath = '{folder}/{name}'.format(
            folder=app.config['UPLOAD_FOLDER'], name=filename
        )
        queryimagename = result.buildindex(filepath)
        htmlstr = result.queryresults(queryimagename)
        return render_template(
            'predicted.html',
            htmlstr=htmlstr,
            filename=filename,
            mode=mode, str=str
        )
    else:
        filepath = '../{folder}/{name}'.format(
            folder=app.config['UPLOAD_FOLDER'], name=filename
        )
        try:
            os.chdir('./darknet')
            # 复杂模型
            if mode == COMPLEX_MODE:
                detect_cmd = WEIGHT_CMD
            # 简版模型
            elif mode == SIMPLE_MODE:
                detect_cmd = TINY_WEIGHT_CMD
            r = os.popen(detect_cmd + filepath)
            output_info = r.readlines()
            names, cvs = get_cr(output_info)
            tsp = int(time.time())
            out_image = '../static/predictions/predictions_{tsp}.png'.format(tsp=tsp)
            os.system('mv predictions.png  {target}'.format(target=out_image))
        except OSError as err:
            print err
        finally:
            os.chdir('../')
        return render_template(
            'predicted.html', filename=filename,
            mode=mode, str=str, names=names,
            cvs=cvs, enumerate=enumerate, tsp=str(tsp)
        )


@app.route('/my', methods=['GET', 'POST'])
def my():
    return render_template('my.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("您已成功退出系统!")
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
