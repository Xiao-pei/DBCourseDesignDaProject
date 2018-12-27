# -*- coding: utf-8 -*-
__author__ = 'Xiao Pei'

from flask import Flask, g, session, render_template, request, jsonify, flash, redirect, url_for
import hashlib
import sqlite3
import datetime
import time
import config
from forms import LoginForm, RegisterForm, UpdateForm, SearchForm

app = Flask(__name__)
app.config.from_object('config')
course_choices = [(datetime.timedelta(hours=8, minutes=15), '1st'),
                  (datetime.timedelta(hours=9, minutes=10), '2nd'),
                  (datetime.timedelta(hours=10, minutes=15), '3rd'),
                  (datetime.timedelta(hours=11, minutes=10), '4th'),
                  (datetime.timedelta(hours=13, minutes=50), '5th'),
                  (datetime.timedelta(hours=14, minutes=45), '6th'),
                  (datetime.timedelta(hours=15, minutes=40), '7th'),
                  (datetime.timedelta(hours=16, minutes=45), '8th'),
                  (datetime.timedelta(hours=17, minutes=45), '9th'),
                  (datetime.timedelta(hours=19, minutes=20), '10th')]
time_to_course = {'815': '1th', '910': '2th', '1015': '3th', '1110': '4th', '1350': '5th',
                  '1445': '6th', '1540': '7th', '1645': '8th', '1745': '9th', '1920': '第10th'}


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
    if session.get('user_id') is not None:
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
    value = time.localtime(int(t))
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
                # 更新最后登陆时间
                g.db.execute('UPDATE user SET last_login_time = ? '
                             'WHERE username=? AND pass_hash=?', [get_time(), name, md5_user_psw(name, password)])
                return redirect(url_for('user_profile', user_id=session.get('user_id')))  # 成功
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
    if session.get('user_id') is not None:
        cursor = g.db.execute('SELECT * FROM user WHERE id=? ', [user_id])
        res = cursor.fetchone()
        if res is None:
            return render_template('404.html')
        else:
            tel = None
            new_message, new_reserve = 0, 0
            reserves = []
            info = {'username': res[1], 'real_name': res[3], 'tel': res[4], 'last_login_time': time_to_date(res[5]),
                    'user_type': res[6]}
            if str(user_id) == str(session.get('user_id')):
                display_message = 0
            else:
                display_message = 1
            if str(user_id) == str(session.get('user_id')) or session.get('user_type') == 1:
                tel = res[4]
                cursor_reserve = g.db.execute('SELECT * FROM reserve WHERE user_id=? ', [user_id])
                data = cursor_reserve.fetchall()
                for line in data:  # 该用户的预约记录
                    cursor_room = g.db.execute('SELECT region, address, room_name FROM room WHERE id=? ', [line[2]])
                    address = cursor_room.fetchone()
                    begin_time, end_time = time.localtime(line[4]), time.localtime(line[5])
                    apply_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(line[6]))
                    date = time.strftime("%Y-%m-%d", begin_time)
                    begin_course = time_to_course[str(begin_time.tm_hour) + str(begin_time.tm_min)]
                    end_course = time_to_course[str(end_time.tm_hour) + str(end_time.tm_min)]
                    reserves.append({'region': address[0], 'address': address[1], 'room_name': address[2],
                                     'result': line[3], 'begin_course': begin_course, 'end_course': end_course,
                                     'apply_date': apply_date, 'date': date, 'reason': line[7]})
                cursor_msg = g.db.execute('SELECT source_id FROM msg WHERE dest_id=? and read=0', [user_id])
                if cursor_msg.fetchone() is not None:
                    new_message = 1
                if session.get('user_type') == 1:  # 若是管理员，查询是否有未处理的预约请求
                    cursor_msg = g.db.execute('SELECT user_id FROM reserve WHERE result=0')
                    if cursor_msg.fetchone() is not None:
                        new_reserve = 1
            return render_template('user_profile.html', display_message=display_message, info=info, user_id=user_id,
                                   tel=tel, reserves=reserves, have_new_message=new_message, have_new_reserve=new_reserve)
    else:
        return redirect(url_for('hello'))


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


@app.route('/search/time', methods=['GET'])
def search_time():
    # 已登陆显示搜索页，未登录跳转回到开始页
    if session.get('user_id') is not None and session.get('user_type') != -1:
        form = SearchForm()
        return render_template('search.html', form=form)
    else:
        return redirect(url_for('hello'))


@app.route('/result', methods=['POST'])
def search_time_result():
    date = request.form.get('dates')
    region = request.form.get('region')
    if date is None:
        flash(message='Please choose date of your reservation.')
        return redirect(url_for('search_time'))
    if region is None:
        flash(message='Please choose region of your reservation.')
        return redirect(url_for('search_time'))
    checkboxes, i = [], 1
    begin, end = -1, -1
    # i 代表第ith
    while i < 11:
        tmpresult = request.form.get('course' + str(i)) is not None
        checkboxes.append(tmpresult)
        if begin != -1 and end != -1 and tmpresult is True:
            flash(message='You cannot select courses like this.')
            return redirect(url_for('search_time'))
        if tmpresult is False and begin != -1 and end == -1:
            end = i - 1
        if tmpresult is True and begin == -1:
            begin = i
        i = i + 1
    if begin == -1 and end == -1:
        flash(message='Please select courses.')
        return redirect(url_for('search_time'))
    begin_date = datetime.datetime.fromtimestamp(int(date)) + course_choices[begin - 1][0]
    end_date = datetime.datetime.fromtimestamp(int(date)) + course_choices[end - 1][0]
    begin_time, end_time = int(time.mktime(begin_date.timetuple())), int(time.mktime(end_date.timetuple()))
    cursor_occupied_room = g.db.execute('SELECT DISTINCT  room_id FROM occupied_room WHERE'
                                        ' start_time>? AND start_time <? OR end_time>? AND end_time<? OR start_time<=? '
                                        'AND end_time>=? AND room_id IN (SElECT id FROM room WHERE region = ?)',
                                        [begin_time, end_time, begin_time, end_time, begin_time, end_time, region])
    cursor_reserve = g.db.execute('SELECT DISTINCT  room_id FROM reserve WHERE '
                                  'start_time>? AND start_time <? OR end_time>? AND end_time<? OR start_time<=? '
                                  'AND end_time>=? AND room_id IN (SElECT id FROM room WHERE region = ?)',
                                  [begin_time, end_time, begin_time, end_time, begin_time, end_time, region])
    cursor_room = g.db.execute('SELECT id, address,room_name,size,multimedia FROM room WHERE region = ?', [region])
    res = cursor_occupied_room.fetchall()
    occupied_room_id = []  # 不可用的教室id
    for line in res:
        occupied_room_id.append(line[0])
    res = cursor_reserve.fetchall()
    for line in res:
        occupied_room_id.append(line[0])
    room_ids = cursor_room.fetchall()
    buliding_names = []
    buildings = []
    for room_id in room_ids:
        if room_id[0] not in occupied_room_id:
            if room_id[1] in buliding_names:
                index = buliding_names.index(room_id[1])
                buildings[index].append({'id': room_id[0], 'address': room_id[1],
                                        'room_name': room_id[2], 'size': room_id[3], 'multimedia': room_id[4]})
            else:
                buliding_names.append(room_id[1])
                buildings.append([{'id': room_id[0], 'address': room_id[1],
                                   'room_name': room_id[2], 'size': room_id[3], 'multimedia': room_id[4]}])

    return render_template('search_result.html', buildings=buildings, buliding_names=buliding_names,
                           date=date, begin=begin, end=end)


@app.route('/reserve/<room_id>', methods=['GET'])
def reserve(room_id):
    if session.get('user_id') is not None and session.get('user_type') != -1:
        if request.method == 'GET':
            date, begin, end = int(request.args.get('date')), int(request.args.get('begin')), int(
                request.args.get('end'))
            cursor_room = g.db.execute('SELECT id, address,room_name,size FROM room WHERE id = ?', [room_id])
            res = cursor_room.fetchone()
            if res is None:
                return redirect(url_for('search_time'))
            address, room_name = res[1], res[2]
            begin_date = datetime.datetime.fromtimestamp(date) + course_choices[begin - 1][0]
            end_date = datetime.datetime.fromtimestamp(date) + course_choices[end - 1][0]
            begin_time, end_time = int(time.mktime(begin_date.timetuple())), int(time.mktime(end_date.timetuple()))
            return render_template('reserve.html', address=address, room_name=room_name, size=res[3],
                                   room_id=room_id, begin_time=begin_time, end_time=end_time)
    else:
        return redirect(url_for('hello'))


@app.route('/reserve/result', methods=['POST'])
def reserve_result():
    if session.get('user_id') is not None and session.get('user_type') != -1:
        begin_time, end_time = request.form.get('begin_time'), request.form.get('end_time')
        room_id = request.form.get('room_id')
        reason = request.form.get('reason')
        cursor_occupied_room = g.db.execute('SELECT DISTINCT  room_id FROM occupied_room WHERE '
                                            '(start_time>? AND start_time<? OR end_time>? AND end_time<? OR '
                                            'start_time<=?AND end_time>=? )AND room_id=?',
                                            [begin_time, end_time, begin_time, end_time, begin_time, end_time,
                                             room_id])
        cursor_reserve = g.db.execute('SELECT DISTINCT  room_id FROM reserve WHERE '
                                      '(start_time>? AND start_time <? OR end_time>? AND end_time<? OR start_time<=? '
                                      'AND end_time>=?) AND room_id=?',
                                      [begin_time, end_time, begin_time, end_time, begin_time, end_time, room_id])
        if cursor_reserve.fetchone() is None and cursor_occupied_room.fetchone() is None:
            now = int(get_time())
            g.db.execute('insert into reserve(user_id, room_id, result, start_time, end_time,'
                         'apply_time, reason)values(?,?,?,?,?,?,?)',
                         [session.get('user_id'), room_id, 0, begin_time,
                          end_time, now, reason])
            return redirect(url_for('user_profile', user_id=session.get('user_id')))
        else:
            return redirect(url_for('search_time'))
    else:
        return redirect(url_for('hello'))


@app.route('/reserve/management', methods=['POST', 'GET'])
def reserve_management():
    if session['user_type'] == 1:
        if request.method == 'GET':
            cursor_reserves = g.db.execute('SELECT * FROM reserve WHERE result=0')
            res = cursor_reserves.fetchall()
            reserves, empty = [], 1
            for line in res:
                empty = 0
                cursor = g.db.execute('SELECT region,address,room_name FROM room WHERE id=?', [line[2]])
                room_info = cursor.fetchone()
                begin_time, end_time = time.localtime(line[4]), time.localtime(line[5])
                apply_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(line[6]))
                date = time.strftime("%Y-%m-%d", begin_time)
                address =room_info[2]+ ", " + room_info[1] + ", " + room_info[0]
                begin_course = time_to_course[str(begin_time.tm_hour) + str(begin_time.tm_min)]
                end_course = time_to_course[str(end_time.tm_hour) + str(end_time.tm_min)]
                reserves.append({'user_id': line[1], 'apply_time': apply_date, 'date': date,
                                 'begin_course': begin_course, 'end_course': end_course, 'address': address,
                                 'reason': line[7], 'reserve_id': line[0]})
            return render_template('reserve_management.html', reserves=reserves, empty=empty)
        else:
            reserve_id = request.form.get('reserve_id')
            if request.form.get('submit') == 'Approve':
                g.db.execute('UPDATE reserve SET result=? WHERE id=?', [1, reserve_id])
            else:
                g.db.execute('UPDATE reserve SET result=? WHERE id=?', [2, reserve_id])
            return redirect(url_for('reserve_management'))
    else:
        return redirect(url_for('hello'))


# 管理员查看所有消息
@app.route('/reserve/all', methods=['GET'])
def reserve_all():
    if session['user_type'] == 1:
        cursor_reserves = g.db.execute('SELECT * FROM reserve WHERE result!=0')
        res = cursor_reserves.fetchall()
        reserves = []
        for line in res:
            cursor = g.db.execute('SELECT region,address,room_name FROM room WHERE id=?', [line[2]])
            room_info = cursor.fetchone()
            begin_time, end_time = time.localtime(line[4]), time.localtime(line[5])
            apply_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(line[6]))
            date = time.strftime("%Y-%m-%d", begin_time)
            address = room_info[0] + room_info[1] + room_info[2]
            begin_course = time_to_course[str(begin_time.tm_hour) + str(begin_time.tm_min)]
            end_course = time_to_course[str(end_time.tm_hour) + str(end_time.tm_min)]
            status = 'Rejected'
            if line[3] == 1:
                status = 'Approved'
            reserves.append({'user_id': line[1], 'apply_time': apply_date, 'date': date,
                             'begin_course': begin_course, 'end_course': end_course, 'address': address,
                             'reason': line[7], 'reserve_id': line[0], 'status': status})
        return render_template('reserve_all.html', reserves=reserves)
    else:
        redirect(url_for('hello'))


# send a message to <user_id>
@app.route('/send/message/<user_id>', methods=['GET'])
def send_message(user_id):
    if session.get('user_id') is not None and session.get('user_id') != int(user_id):
        username = request.args.get('username')
        return render_template('new_message.html', username=username, user_id=user_id)
    else:
        return redirect(url_for('hello'))


@app.route('/message/<user_id>', methods=['GET'])
def message(user_id):
    if str(session.get('user_id')) == user_id:
        cursor = g.db.execute('SELECT source_id, resp_text, resp_time, read, id FROM msg WHERE dest_id=?', [user_id])
        result = cursor.fetchall()
        msg_id = request.args.get('msg_id')
        message_view = None
        messages = []
        for line in result:
            username_cursor = g.db.execute('SELECT username FROM user WHERE id=?', [line[0]])
            username = username_cursor.fetchone()[0]
            if str(line[4]) == msg_id:
                message_view = {'msg_id': line[4], 'source_id': line[0], 'text': line[1],
                                'resp_time': time_to_date(line[2])}
                g.db.execute('UPDATE msg SET read = ? WHERE id=?', [1, msg_id])
                messages.append({'msg_id': line[4], 'source_id': line[0], 'preview': line[1][0:12], 'read': 1,
                                'resp_time': time_to_date(line[2]), 'username': username})
            else:
                messages.append({'msg_id': line[4], 'source_id': line[0], 'preview': line[1][0:12],
                                 'read': int(line[3]), 'resp_time': time_to_date(line[2]), 'username': username})
        return render_template('message.html', messages=messages, message_view=message_view)
    else:
        return redirect(url_for('hello'))


# all sent message of <user_id>
@app.route('/message/<user_id>/sent', methods=['POST', 'GET'])
def message_sent(user_id):
    if str(session.get('user_id')) == user_id:
        if request.method == 'POST':
            dest_id = request.form.get('dest_id')
            resp_text = request.form.get('msg')
            cursor = g.db.execute('SELECT id FROM user WHERE id=?', [dest_id])
            if cursor.fetchone() is None:
                return 'No such user'
            else:
                now = int(get_time())
                g.db.execute('INSERT INTO msg(source_id,dest_id,resp_text,resp_time,read) values(?,?,?,?,?)',
                             [user_id, dest_id, resp_text, now, 0])
                return redirect(url_for('message_sent', user_id=user_id))
        else:
            cursor = g.db.execute('SELECT dest_id, resp_text, resp_time, read FROM msg WHERE source_id=?', [user_id])
            result = cursor.fetchall()
            messages = []
            for line in result:
                messages.append({'dest_id': line[0], 'resp_text': line[1], 'read': int(line[3]),
                                 'resp_time': time_to_date(line[2])})
            return render_template('message_sent.html', messages=messages)
    else:
        return redirect(url_for('hello'))


@app.route('/lock', methods=['POST'])
def lock():
    if session.get('user_type') == 1:
        user_id = request.form.get('user_id')
        action = request.form.get('submit')
        if action == 'Unlock user':
            g.db.execute('UPDATE user SET type=0 WHERE id=?', [user_id])
        else:
            g.db.execute('UPDATE user SET type=-1 WHERE id=?', [user_id])
        return redirect(url_for('user_profile', user_id=user_id))
    return url_for('hello')


@app.route('/logout')
def logout():
    # 如果会话中有用户id就删除它。
    session.pop('user_id', None)
    session.pop('user_type', None)
    return url_for('hello')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
