# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

__author__ = 'Xiao Pei'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, RadioField, validators, FormField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.form import BaseForm
import time
import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN IN')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    real_name = StringField('Real Name', validators=[DataRequired()])
    tel = IntegerField('Telephone Number', validators=[DataRequired(message='123456')])
    submit = SubmitField('REGISTER')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    real_name = StringField('Real Name', validators=[DataRequired()])
    tel = IntegerField('Telephone Number', validators=[DataRequired()])
    submit = SubmitField('Update')


def getdays():
    today = datetime.datetime.now()
    days: List[datetime] = []
    count = 0
    while count <= 7:
        days.append(today + datetime.timedelta(days=count))
        count = count + 1
    return days


class SearchForm(FlaskForm):
    days = getdays()
    choices = []
    for day in days:
        choices.append((int(time.mktime(day.date().timetuple())), day.date().strftime('%m/%d')))

    dates = RadioField('日期', choices=choices, validators=[DataRequired(message="请选择日期")])
    course1 = BooleanField('第01节课')
    course2 = BooleanField('第02节课')
    course3 = BooleanField('第03节课')
    course4 = BooleanField('第04节课')
    course5 = BooleanField('第05节课')
    course6 = BooleanField('第06节课')
    course7 = BooleanField('第07节课')
    course8 = BooleanField('第08节课')
    course9 = BooleanField('第09节课')
    course10 = BooleanField('第10节课')
    region = RadioField('校区', choices=[('望江', '望江'), ('华西', '华西'), ('江安', '江安')], default='江安')
    submit = SubmitField('Submit')


