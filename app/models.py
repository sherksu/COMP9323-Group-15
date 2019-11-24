"""
# Project           : COMP9323
# Author            : Heping Zhao
# Date created      : 25/10/2019
# Description       : Login User Class
"""
from app import db as pydb, login_manager
from flask import current_app
import jwt


class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @login_manager.user_loader
    def load_user(username):
        u = pydb.users.find_one({"username": username})
        if not u:
            return None
        return User(u['username'])

    def generate_reset_password(self):
        return jwt.encode({'username': self.username}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def check_reset_password(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return data
        except:
            return

    def find_email(self):
        x = pydb.users.find_one({'username': self.username})
        return x['email']
