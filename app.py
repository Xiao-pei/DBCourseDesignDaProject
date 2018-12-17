
__author__ = 'Xiao Pei'

from flask import Flask, g, session, render_template, request, jsonify, flash, abort
import hashlib
import sqlite3
import datetime
import time
import config
from forms import LoginForm, RegisterForm


app = Flask(__name__)
app.config.from_object('config')


@app.before_request
def before_req():
    g.db = sqlite3.connect(app.config['DATABASE'])


@app.teardown_request
def teardown_req(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.commit()
        db.close()


@app.route('/')
def hello():
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


@app.route('/login', methods=['POST', 'GET'])
def test():
    form = LoginForm()
    if request.method == 'GET':
        return 'My man'
    else:
        if form.validate_on_submit():
            name, password = request.form["username"], request.form['password']
            cursor = g.db.execute('SELECT id,type FROM user WHERE username=? '
                                  'AND pass_hash=?', [name, md5_user_psw(name, password)])
            res = cursor.fetchone()
            if res is not None:
                session['user_id'] = res[0]
                session['user_type'] = res[1]
                session['logged_in'] = True
                g.db.execute('UPDATE user SET last_login_time = ? '
                             'WHERE username=? AND pass_hash=?', [get_time(), name, md5_user_psw(name, password)])
                return jsonify({'code': 200})
            flash('用户名或密码错误')
            return render_template('login.html', title='Sign In', form=form)
        else:
            return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name, password = request.form["username"], request.form['password']
        real_name, tel = request.form["real_name"], request.form['tel']
        cursor = g.db.execute('SELECT id FROM user WHERE username=? ', [name])
        res = cursor.fetchone()
        if res is not None:
            flash("用户名已被注册")
            return render_template('register.html', title='Register', form=form)
        g.db.execute('insert into user(username, pass_hash, real_name, tel,last_login_time,type) values (?,?,?,?,?,?)',
                     [name, md5_user_psw(name, password), real_name, tel, 1, 0])
        return jsonify({'code': 200})
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>', methods=['GET'])
def user_profile(username):
    cursor = g.db.execute('SELECT * FROM user WHERE username=? ', [username])
    res = cursor.fetchone()
    if res is None:
        return jsonify({'code': 404})
    else:
        info = {'username': res[1], 'real_name': res[3], 'tel': res[4], 'last_login_time': res[5]}
        return render_template('user_profile.html', title='Register',username=username, info=info)


@app.route('/logout')
def logout():
    # 如果会话中有用户id就删除它。
    session.pop('user_id', None)
    session['logged_in'] = False
    return jsonify({'code': 200})


if __name__ == '__main__':
    app.run()
