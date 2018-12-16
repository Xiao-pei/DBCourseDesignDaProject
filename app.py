
__author__ = 'Xiao Pei'

from flask import Flask, g, session, render_template, request, jsonify, abort
import hashlib
import sqlite3
import config
from forms import LoginForm


app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


def md5_user_psw(name, psw):
    before_hash = name + psw
    # 求 MD5(username+password)
    hl = hashlib.md5()
    hl.update(before_hash.encode(encoding='utf-8'))
    return hl.hexdigest()


@app.route('/login', methods=['POST', 'GET'])
def test():
    form = LoginForm()
    if request.method == 'GET':
        return 'My man'
    else:
        if form.validate_on_submit() and request.form['username'] == 'xiaopc':
            return jsonify({'code': 200})
        else:
            return render_template('login.html', title='Sign In', form=form)


@app.route('/app/logout')
def logout():
    # 如果会话中有用户id就删除它。
    session.pop('user_id', None)
    return jsonify({'code': 200})


if __name__ == '__main__':
    app.run()
