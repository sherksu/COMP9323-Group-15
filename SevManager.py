"""
# Project           : COMP9323
# Author            : Group 15
# Date created      : 25/10/2019
# Description       : Application Management
"""

from flask_script import Manager, Shell, Server
from app import create_app, db, socketio
import sys

# basic config
host = "localhost"
port = 6333


class socket_server(Server):
    def __call__(self, app, host, port, use_debugger, use_reloader,
                 threaded, processes, passthrough_errors, ssl_crt, ssl_key):
        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
                if sys.stderr.isatty():
                    print("Debugging is on. DANGER: Do not allow random users to connect to this server.", file=sys.stderr)
        if use_reloader is None:
            use_reloader = use_debugger

        if None in [ssl_crt, ssl_key]:
            ssl_context = None
        else:
            ssl_context = (ssl_crt, ssl_key)
        """
        Deployment
        There are many options to deploy a Flask-SocketIO server, ranging from simple to the insanely complex. In this section, the most commonly used options are described.

        Embedded Server
        The simplest deployment strategy is to have eventlet or gevent installed, and start the web server by calling socketio.run(app) as shown in examples above. This will run the application on the eventlet or gevent web servers, whichever is installed.
        """
        socketio.run(app,
                host=host,
                port=port,
                debug=use_debugger,
                use_reloader=use_reloader,
                **self.server_options,
                max_size=1024)  #max number of socket client


server = socket_server(host, port)

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
