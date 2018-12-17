# -*- coding: utf-8 -*-

__author__ = 'Xiao Pei'

import sqlite3
import os

if os.path.isfile('./test.db'):
    exit()

conn = sqlite3.connect('test.db')

with conn:
    cur = conn.cursor()
    # id 主键；username 用户名；pass_hash md5(username+password)； real_name 真实姓名；tel 电话；type 0为用户 1 为管理员
    cur.execute('''create table user 
                        (
                            id integer primary key autoincrement,
                            username varchar(20) not null unique,
                            pass_hash varchar(64) not null,
                            real_name varchar(64) not null,
                            tel integer not null,
                            last_login_time integer not null ,
                            type int not null
                        )''')
    # id 主键；region 校区；address 地址；size 大小
    cur.execute('''create table room 
                        (
                            id integer primary key autoincrement,
                            region varchar(20) not null,
                            address varchar(64) not null,
                            size int not null
                        )''')
    # 本来就被占用的教室信息表；
    cur.execute('''create table occupied_room 
                        (
                            id integer primary key autoincrement,
                            room_id integer not null,
                            start_time int not null,
                            end_time int not null,
                            foreign key(room_id) references room(id)
                        )''')
    # 预约信息表；id 主键；user_id 预约人；room_id 预约房间；result 0为等待 1为同意 2为拒绝；start_time 起始时间（unix时间戳）；
    # end_time 结束时间（unix时间戳）；reason 申请理由；
    cur.execute('''create table reserve
                        (
                             id integer primary key autoincrement,
                             user_id integer not null,
                             room_id integer not null,
                             result integer not null,
                             start_time int not null,
                             end_time int not null,
                             reason text,
                             foreign key(room_id) references room(id),
                             foreign key(user_id) references user(id)
                        )''')
    # 消息推送表；source_id 发消息人id；dest_id 收消息人id ；resp_text 回复内容；resp_time 回复时间；
    cur.execute('''create table msg
                        (
                            id integer primary key autoincrement,
                            source_id integer ,
                            dest_id integer not null,
                            resp_text text,
                            resp_time integer not null,
                            foreign key (source_id) references user(id),
                            foreign key (dest_id) references user(id)
                        )''')
    cur.execute('''insert into user(username, pass_hash, real_name,tel,last_login_time,type)
    values (\'admin\', \'f6fdffe48c908deb0f4c3bd36c032e72\', \'管理员\',555,100, 1)''')
    cur.execute('''insert into user(username, pass_hash, real_name,tel,last_login_time,type)
    values (\'xiaopc\', \'5aa8a6c678dbb5435d01f813c3dac7cc\', \'Xiaopc\',666,100, 0)''')

