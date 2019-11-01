from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileField
from app import db as pydb


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm = PasswordField('Repeat', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

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
    submit = SubmitField('Log in')


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


class RoleCreateForm(FlaskForm):
    image = FileField(u'Choose Your Avatar', validators=[FileRequired()])
    rolename = StringField('Role Name', validators=[DataRequired(), Length(min=2, max=30)])
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')])
    slogan = StringField('Personal Slogan', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')

    def validate_rolename(self, rolename):
        role = pydb.users.find_one({'rolename': rolename.data})
        if role:
            raise ValidationError("Role name has been used, Please try again!")
