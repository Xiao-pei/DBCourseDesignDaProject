# -*- coding: utf-8 -*-

__author__ = 'Xiao Pei'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    real_name = StringField('Real Name', validators=[DataRequired()])
    tel = IntegerField('Telephone Number', validators=[DataRequired()])
    submit = SubmitField('Register')
