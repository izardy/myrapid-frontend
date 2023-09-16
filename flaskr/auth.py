import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from flaskr.db import get_db
from flask import send_from_directory
from flask_login import LoginManager
login_manager = LoginManager()

bp = Blueprint('auth', __name__, url_prefix='/auth')

####################################################################################

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        username = request.form['username']
        password = request.form['password']
        countryInput = request.form['countryInput']
        stateInput = request.form['stateInput']
        districtInput = request.form['districtInput']
        phone = request.form['phone']
        db = get_db()
        error = None

        if not nickname:
            error = 'Nickname is required.'        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not countryInput:
            error = 'Country of origin is required.'
        elif not stateInput:
            error = 'State of origin is required'
        elif not districtInput:
            error = 'District of origin is required'
        elif not phone:
            error = 'User phone is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (nickname, username, password, countryInput, stateInput, districtInput, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nickname, username, generate_password_hash(password), countryInput, stateInput, districtInput, phone),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

####################################################################################

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

####################################################################################

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#################################################################################### [SHOW USER INFO]

@bp.route('/user_view')
def list_info():
    db = get_db()
    user = db.execute(
        'SELECT id, username, nickname, phone, countryInput, stateInput, districtInput'
        ' FROM user'
        ' WHERE username = ?',(g.user['username'],)
        #' ORDER BY id ASC'
    ).fetchone()
    return render_template('auth/user_view.html',user=user)

####################################################################################

def get_user(id):
    user = get_db().execute(
        'SELECT id, username, nickname, phone, countryInput, stateInput, districtInput'
        ' FROM user'
        ' WHERE id = ?',(id,)
    ).fetchone()

    if user is None:
        abort(404, f"ID {id} doesn't exist.")

    return user

####################################################################################

@bp.route('/<int:id>/user_update', methods=('GET', 'POST'))
def user_update(id):
    user = get_user(id)
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        divisionInput = request.form['divisionInput']
        officeInput = request.form['officeInput']
        unitInput = request.form['unitInput']
        error = None

        if not old_password:
            error = 'Password is required.'
        
        if not check_password_hash(user['password'], old_password):
            error = 'Incorrect password.'

        if not new_password:
            error = 'Password is required.'
        
        if not divisionInput:
            error = 'Division name is required.'

        if not officeInput:
            error = 'Office name is required.'
        
        if not unitInput:
            error = 'Unit name is required.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE user SET password = ?, divisionInput = ?, officeInput = ?, unitInput = ?'
                ' WHERE id = ?',
                (generate_password_hash(new_password), divisionInput, officeInput, unitInput, id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('auth/user_update.html', user=user)

####################################################################################

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

