from flask_mail import Message
from app import mail
from SevManager import app
from flask import current_app, render_template
from threading import Thread


def send_asunc_mail(apps, msg):
    with apps.app_context():
        mail.send(msg)


def send_reset_password_mail(user, token):
    msg = Message('[Data Hunter Team]Reset your password',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.find_email()],
                  html=render_template('/guide/reset_password_mail.html', user=user, token=token))
    Thread(target=send_asunc_mail, args=(app, msg, )).start()
