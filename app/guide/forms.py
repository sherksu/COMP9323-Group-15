"""
# Project           : COMP9323
# Author            : Heping Zhao
# Date created      : 25/10/2019
# Description       : GUIDE SYSTEM -- FLASK-WTF forms to create tables
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileField
from app import db as pydb


class RegisterForm(FlaskForm):
    image = FileField(u'Choose Your Avatar', validators=[FileRequired()])
    username = StringField('Username', validators=[DataRequired(message='username can not be empty'), Length(min=2, max=30, message='The length between 2 and 30')])
    password = PasswordField('Password', validators=[DataRequired(message='password can not be empty'), Length(min=6, max=30, message='The length between 6 and 30')])
    confirm = PasswordField('Confirm', validators=[DataRequired(message='password can not be empty'), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(message='email can not be empty'), Email()])
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')])
    submit = SubmitField('create!')

    def validate_username(self, username):
        user = pydb.users.find_one({'username': username.data})
        if user:
            raise ValidationError("Username has been used, Please try again!")

    def validate_email(self, email):
        user = pydb.users.find_one({'email': email.data})
        if user:
            raise ValidationError("Email has been used, Please try again")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    rem = BooleanField('Check me out')
    submit = SubmitField('Log In')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = pydb.users.find_one({'email': email.data})
        if not user:
            raise ValidationError("Email does not exist")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm = PasswordField('Repeat', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
