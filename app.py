
__author__ = 'Xiao Pei'

from flask import Flask, g, session, render_template, request, jsonify, flash, abort, redirect, url_for
import hashlib
import sqlite3
import datetime
import time
import config
from forms import LoginForm, RegisterForm, UpdateForm, SearchForm


app = Flask(__name__)
app.config.from_object('config')
course_choices = [(datetime.timedelta(hours=8, minutes=15), '第01节课'),
                  (datetime.timedelta(hours=9, minutes=10), '第02节课'),
                  (datetime.timedelta(hours=10, minutes=15), '第03节课'),
                  (datetime.timedelta(hours=11, minutes=10), '第04节课'),
                  (datetime.timedelta(hours=13, minutes=50), '第05节课'),
                  (datetime.timedelta(hours=14, minutes=45), '第06节课'),
                  (datetime.timedelta(hours=15, minutes=40), '第07节课'),
                  (datetime.timedelta(hours=16, minutes=45), '第08节课'),
                  (datetime.timedelta(hours=17, minutes=45), '第09节课'),
                  (datetime.timedelta(hours=19, minutes=20), '第10节课')]


@app.before_request
def before_req():
    g.db = sqlite3.connect(app.config['DATABASE'])


@app.teardown_request
def teardown_req(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.commit()
        db.close()


# 首页，待修改
@app.route('/')
def hello():
    if session.get('logged_in') is not None:
        return redirect(url_for('user_profile', user_id=session['user_id']))
    else:
        form = LoginForm()
        return render_template('login.html', title='Sign In', form=form)


def md5_user_psw(name, psw):
    before_hash = name + psw
    # 求 MD5(username+password)
    hl = hashlib.md5()
    hl.update(before_hash.encode(encoding='utf-8'))
    return hl.hexdigest()


def get_time():
    return time.mktime(datetime.datetime.now().timetuple())


def time_to_date(t):
    value = time.localtime(t)
    date = time.strftime('%Y-%m-%d %H:%M', value)
    return date


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name, password = request.form["username"], request.form['password']
            cursor = g.db.execute('SELECT id,type FROM user WHERE username=? '
                                  'AND pass_hash=?', [name, md5_user_psw(name, password)])
            res = cursor.fetchone()
            if res is not None:
                session['user_id'] = res[0]
                session['user_type'] = res[1]
                session['logged_in'] = True
                # 更新最后登陆时间
                g.db.execute('UPDATE user SET last_login_time = ? '
                             'WHERE username=? AND pass_hash=?', [get_time(), name, md5_user_psw(name, password)])
                return jsonify({'code': 200})  # 成功
            flash('用户名或密码错误')  # 否则form内容有错
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # form提交并格式有效
        name, password, confirm = request.form["username"], request.form['password'], request.form['password_confirm']
        real_name, tel = request.form["real_name"], request.form['tel']
        if password != confirm:
            # 密码不一致返回
            flash(message='两次密码不一致')
            return render_template('register.html', title='Register', form=form)
        cursor = g.db.execute('SELECT id FROM user WHERE username=? ', [name])
        res = cursor.fetchone()
        if res is not None:
            # 重名返回
            flash(message='用户名已被注册')
            return render_template('register.html', title='Register', form=form)
        g.db.execute('insert into user(username, pass_hash, real_name, tel,last_login_time,type) values (?,?,?,?,?,?)',
                     [name, md5_user_psw(name, password), real_name, tel, 1, 0])
        return jsonify({'code': 200})  # 注册成功
    return render_template('register.html', title='Register', form=form)  # 其余情况返回注册页


# 查看用户信息
@app.route('/user/<user_id>', methods=['GET'])
def user_profile(user_id):
    cursor = g.db.execute('SELECT * FROM user WHERE id=? ', [user_id])
    res = cursor.fetchone()
    if res is None:
        return jsonify({'code': 404})
    else:
        info = {'username': res[1], 'real_name': res[3], 'tel': res[4], 'last_login_time': time_to_date(res[5])}
        return render_template('user_profile.html', title='Register', username=res[1], info=info)


# 更新用户信息
@app.route('/user/<user_id>/update', methods=['GET', 'POST'])
def user_profile_update(user_id):
    form = UpdateForm()
    cursor = g.db.execute('SELECT * FROM user WHERE id=? ', [user_id])
    res = cursor.fetchone()
    if res is None:
        return jsonify({'code': 404})  # 没有改用户 404
    if session['user_id'] == res[0]:
        if request.method == 'POST' and form.validate_on_submit():  # 提交了form
            name, password = request.form['username'], request.form['password']
            real_name, tel = request.form["real_name"], request.form['tel']
            if md5_user_psw(res[1], password) == res[2]:  # 提交了form且密码正确
                g.db.execute('UPDATE user SET username=?,pass_hash=?,real_name=?,tel=? WHERE id=?',
                             [name, md5_user_psw(name, password), real_name, tel, user_id])
                return redirect(url_for('user_profile', user_id=session['user_id']))
            else:
                flash(message='password error')
                return render_template('update.html', title='Update', form=form)
        else:  # 没有提交form
            form.username.data = res[1]
            form.real_name.data = res[3]
            form.tel.data = res[4]
            return render_template('update.html', title='Update', form=form)
    # 不是本用户访问
    return redirect(url_for('hello'))  # 待修改


@app.route('/logout')
def logout():
    # 如果会话中有用户id就删除它。
    session.pop('user_id', None)
    session['logged_in'] = False
    return jsonify({'code': 200})


if __name__ == '__main__':
    app.run()
