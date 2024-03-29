from . import guide
from flask import render_template, flash, redirect, url_for
from app import secure
from app import db as pydb
from app.models import User
from .forms import RegisterForm, LoginForm, PasswordResetForm, ResetPasswordForm, RoleCreateForm
from flask_login import login_required, login_user, current_user, logout_user
from .email import send_reset_password_mail
from bson import ObjectId
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@guide.route('/role_create', methods=['GET', 'POST'])
@login_required
def index():
    user = pydb.users.find_one({'username': current_user.username})
    try:
        role = user['rolename']
        if role:
            return redirect(url_for('guide.world_map'))
    except KeyError:
        pass
    form = RoleCreateForm()
    if form.validate_on_submit():
        image = form.image.data
        if image.filename == '':
            flash('No selected file')
            return render_template('/guide/index.html', form=form)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join('app', 'static', 'filedata', filename))
            avatar = '/static/filedata/' + filename
        rolename = form.rolename.data
        gender = dict(form.gender.choices).get(form.gender.data)
        slogan = form.slogan.data
        pydb.users.update_one({'username': current_user.username},
                              {'$set': {'avatar': avatar, 'rolename': rolename, 'gender': gender, 'slogan': slogan}})
        return redirect(url_for('guide.world_map'))
    return render_template('/guide/index.html', form=form)


@guide.route('/role_change', methods=['GET', 'POST'])
@login_required
def role_change():
    form = RoleCreateForm()
    user = pydb.users.find_one({'username': current_user.username})
    role = user['rolename']
    if role:
        if form.validate_on_submit():
            image = form.image.data
            if image.filename == '':
                flash('No selected file')
                return render_template('/guide/index.html', form=form)
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join('app', 'static', 'filedata', filename))
                avatar = '/static/filedata/' + filename
            rolename = form.rolename.data
            gender = dict(form.gender.choices).get(form.gender.data)
            slogan = form.slogan.data
            pydb.users.update_one({'username': current_user.username},
                                  {'$set': {'avatar': avatar, 'rolename': rolename,
                                            'gender': gender, 'slogan': slogan}})
            return redirect(url_for('guide.world_map'))
    else:
        return redirect(url_for('guide.index'))
    return render_template('/guide/change_role.html', form=form)


@guide.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = str(secure.generate_password_hash(form.password.data))
        new_id = ObjectId()
        pydb.users.insert({'username': username, 'password': password, 'email': email})
        flash('Well done! Sign up successfully!', category='success')
        return redirect(url_for('guide.login'))
    return render_template('/guide/signup.html', form=form)


@guide.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            rem = form.rem.data
            user = pydb.users.find_one({'username': username})
            if user and secure.check_password_hash(user['password'].replace("b'", "").replace("'", ""), password):
                user_obj = User(user['username'])
                login_user(user_obj, remember=rem)
                try:
                    role = user['rolename']
                    if role:
                        return redirect(url_for('guide.world_map'))
                except KeyError:
                    return redirect(url_for('guide.index'))
            flash('User does not exist or password is incorrect', category='danger')
        return render_template('/guide/login.html', form=form)
    else:
        return redirect(url_for('guide.world_map'))


@guide.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Well done! Log out successfully', category='success')
    return redirect(url_for('welcome'))


@guide.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('guide.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
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
        return redirect(url_for('guide.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password(token)
        if user:
            pydb.users.update({'username': user['username']},
                              {'$set': {'password': str(secure.generate_password_hash(form.password.data))}})
            flash('Your password has been reset, you can login now.', category='info')
            return redirect(url_for('guide.login'))
        else:
            flash('The user does not exist', category='info')
            return redirect(url_for('guide.login'))
    return render_template('/guide/password_reset.html', form=form)


@guide.route('/world_map', methods=['GET', 'POST'])
def world_map():
    return render_template('/guide/world_map.html')


@guide.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():
    user = pydb.users.find_one({'username': current_user.username})
    avatar = user['avatar']
    slogan = user['slogan']
    gender = user['gender']
    rolename = user['rolename']
    return render_template('/guide/user_profile.html', avatar=avatar, slogan=slogan, gender=gender, rolename=rolename)
