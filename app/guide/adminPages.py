from . import guide
from flask import render_template, flash, redirect, url_for, request
from app import secure
from app import db as pydb
from app.MongoFunction import get_list_of_complete_username
from app.models import User
from .forms import RegisterForm, LoginForm, PasswordResetForm, ResetPasswordForm
from flask_login import login_required, login_user, current_user, logout_user
from .email import send_reset_password_mail
from bson import ObjectId
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@guide.route('/signup', methods=['GET', 'POST'])
def signup():
    global gender
    form = RegisterForm(request.form)
    if request.method == 'POST':
        image = request.files['file']
        if image.filename == '':
            flash('Please choose your avatar!', category='danger')
            return render_template('/guide/signup.html', form=form)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join('app', 'static', 'filedata', filename))
            avatar = '/static/filedata/' + filename
        username = form.username.data
        user = pydb.users.find_one({'username': username})
        if user:
            flash('Username has been used, Please try again!', category='danger')
            return render_template('/guide/signup.html', form=form)
        email = form.email.data
        emailname = pydb.users.find_one({'email': email})
        if emailname:
            flash('Email has been used, Please try again!', category='danger')
            return render_template('/guide/signup.html', form=form)
        if request.form['submit'] == 'M':
            gender = "Male"
        elif request.form['submit'] == 'F':
            gender = "Female"

        password = str(secure.generate_password_hash(form.password.data))
        pydb.users.insert({'avatar': avatar, 'username': username, 'password': password, 'email': email, 'gender': gender})
        flash('Well done! Sign up successfully!', category='success')
        return redirect(url_for('guide.login'))
    return render_template('/guide/signup.html', form=form)


@guide.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm(request.form)
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data
            rem = form.rem.data
            user = pydb.users.find_one({'username': username})
            if user and secure.check_password_hash(user['password'].replace("b'", "").replace("'", ""), password):
                user_obj = User(user['username'])
                login_user(user_obj, remember=rem)
                return redirect(url_for('guide.world_map'))
            else:
                flash('User does not exist or password is incorrect', category='danger')
        return render_template('/guide/login.html', form=form)
    else:
        return redirect(url_for('guide.world_map'))


@guide.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))


@guide.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('guide.world_map'))
    form = PasswordResetForm(request.form)
    if request.method == 'POST':
        email = form.email.data
        user = pydb.users.find_one({'email': email})
        user_obj = User(user['username'])
        token = user_obj.generate_reset_password()
        send_reset_password_mail(user_obj, token)
        flash('Password reset mail has been sent, please check your email.', category='info')
    return render_template('/guide/password_reset.html', form=form)


@guide.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('guide.world_map'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST':
        user = User.check_reset_password(token)
        if user:
            pydb.users.update({'username': user['username']},
                              {'$set': {'password': str(secure.generate_password_hash(form.password.data))}})
            flash('Your password has been reset, you can login now.', category='info')
            return redirect(url_for('guide.login'))
        else:
            flash('The user does not exist', category='info')
            return redirect(url_for('guide.login'))
    return render_template('/guide/password_reset_commit.html', form=form)


@guide.route('/world_map', methods=['GET', 'POST'])
def world_map():
    courses = pydb.courses.find()
    course_ids = [x for x in courses]
    result = []
    for i in course_ids:
        complete = get_list_of_complete_username(current_user.username, i['_id'])
        del i['_id']
        if complete['complete']:
            i.update({"overall": complete['complete'][0]['overall']})
            result.append(i)
        else:
            i.update({"overall": ""})
            result.append(i)
    return render_template('/guide/world_map.html', course=result, lengths=len(result), title="map")


@guide.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():
    user = pydb.users.find_one({'username': current_user.username})
    avatar = user['avatar']
    slogan = user['slogan']
    gender = user['gender']
    rolename = user['rolename']
    return render_template('/guide/user_profile.html', avatar=avatar, slogan=slogan, gender=gender, rolename=rolename)


