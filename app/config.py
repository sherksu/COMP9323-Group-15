from flask_nav import Nav
from flask_nav.elements import *
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-SECRET-KEY'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'A-VERY-LONG-SECRET-KEY'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME') or 'zhaoheping1995'
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD') or 'dxjirqufbpegvzgg'


# navigation setting
nav = Nav()
nav.register_element('top', Navbar(
    '',
    View('Home', 'welcome'),
    View('Login', 'guide.login'),
    View('Sign up', 'guide.signup'),
    View('Logout', 'guide.logout'),
    View('Userprofile', 'guide.user_page')
))
