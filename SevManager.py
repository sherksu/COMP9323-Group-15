"""
# Project           : COMP9323
# Author            : Group 15
# Date created      : 25/10/2019
# Description       : Application Management
"""

from flask_script import Manager, Shell, Server
from app import create_app, db

# basic config
host = "localhost"
port = 5000
server = Server(host, port)

# bind app % manager
app = create_app()
manager = Manager(app)


# shell setting
def app_info():
    return dict(app=app, db=db)


# insert command
manager.add_command("shell", Shell(make_context=app_info))
manager.add_command("runserver", server)


# customer command (maybe later...)
@manager.command
def insert_users():
    name = input("your name: ")
    print(name)


if __name__ == "__main__":
    manager.run()
    # python SevManager.py runserver -d -r
    # d: debug
    # r: reload !
    # h: host
    # p: port
