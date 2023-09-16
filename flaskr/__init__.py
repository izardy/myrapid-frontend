import os
from flask import Flask
from flask import send_from_directory
from flask_login import login_required
from flask_login import LoginManager
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
login_manager = LoginManager()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # db
    from . import db
    db.init_app(app)

    # auth
    from . import auth
    app.register_blueprint(auth.bp)

    # main
    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    #########################
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    #########################

    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view

    #########################

    @app.route('/banana/<path:filename>')
    @login_required
    def banana(filename):
        return send_from_directory(
            os.path.join(app.instance_path, 'banana'),
            filename
    )

    #########################

    return app

