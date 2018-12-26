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

    dates = RadioField('日期', choices=choices, validators=[DataRequired(message="Please choose date of your reservation.")])
    course1 = BooleanField('1st')
    course2 = BooleanField('2nd')
    course3 = BooleanField('3rd')
    course4 = BooleanField('4th')
    course5 = BooleanField('5th')
    course6 = BooleanField('6th')
    course7 = BooleanField('7th')
    course8 = BooleanField('8th')
    course9 = BooleanField('9th')
    course10 = BooleanField('10th')
    region = RadioField('校区', choices=[('望江', 'Wangjiang Campus'), ('华西', 'Huaxi Campus'), ('江安', 'Jiang\'an Campus')], default='江安')
    submit = SubmitField('Submit')


