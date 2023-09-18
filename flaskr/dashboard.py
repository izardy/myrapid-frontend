from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from flask_paginate import Pagination, get_page_args

import functools

from IPython.display import HTML
import pandas as pd
import numpy as np

#################################################################################### [LOAD USER ID]

bp = Blueprint('dashboard', __name__)

def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#################################################################################### [LOGIN CHECK]

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#################################################################################### [DEPOT INFO AS MAIN PAGE]

@bp.route('/')
@login_required
def index():
    return render_template('dashboard/depot.html')

#################################################################################### [CAPTAIN INFO]

@bp.route('/captain')
@login_required
def captain():
    return render_template('dashboard/captain.html')

#################################################################################### [BAS INFO]

@bp.route('/bas')
@login_required
def bas():
    return render_template('dashboard/bas.html')

#################################################################################### [TRIP INFO]

@bp.route('/trip')
@login_required
def trip():
    return render_template('dashboard/trip.html')

#################################################################################### [ADD idea]

@bp.route('/add_idea', methods = ['POST','GET'])
@login_required
def add_idea():
    if request.method == 'POST':
        idea_name =request.form['idea_name']
        idea_status=request.form['idea_status']
        idea_statement =request.form['idea_statement']
        idea_issue =request.form['idea_issue']
        idea_strategy =request.form['idea_strategy']

        issue_depot =request.form['issue_depot']
        issue_driver =request.form['issue_driver']
        issue_bus =request.form['issue_bus']
        issue_trip =request.form['issue_trip']
        pitch_date =request.form['pitch_date']
        phone =request.form['phone']

        error = None

        if not idea_name:
            error = 'idea name is required.'
        elif not idea_statement:
            error = 'idea statement is required.'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                "INSERT INTO idea (idea_name,idea_status,idea_statement,idea_issue,idea_strategy,issue_depot,issue_driver,issue_bus,issue_trip,pitch_date,phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (idea_name,idea_status,idea_statement,idea_issue,idea_strategy,issue_depot,issue_driver,issue_bus,issue_trip,pitch_date,phone),
            )
            db.commit()
            return redirect(url_for('dashboard.list_idea'))
    return render_template('dashboard/add_idea.html')

#################################################################################### [DELETE idea]

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_idea(id):
    get_idea(id,)
    db = get_db()
    db.execute('DELETE FROM idea WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard.list_idea'))

#################################################################################### [LIST idea]

@bp.route('/list_idea')
@login_required
def list_idea():
    db = get_db()
    ideas = db.execute(
        'SELECT id,idea_name,idea_status,idea_statement,idea_issue,idea_strategy,issue_depot,issue_driver,issue_trip,pitch_date,phone'
        ' FROM idea'
        ' WHERE phone = ?',(g.user['phone'],)
        #' ORDER BY id ASC'
    ).fetchall()
    return render_template('dashboard/list_idea.html', ideas=ideas)

####################################################################################

def get_idea(id):
    idea = get_db().execute(
        'SELECT id,idea_name,idea_status,idea_statement,idea_issue,idea_strategy,issue_depot,issue_driver,issue_trip,pitch_date,phone'
        ' FROM idea'
        ' WHERE id = ?',(id,)
    ).fetchone()

    if idea is None:
        abort(404, f"idea id {id} doesn't exist.")

    return idea

#################################################################################### [UPDATE idea]

@bp.route('/<int:id>/update_idea', methods=('GET', 'POST'))
@login_required
def update_idea(id):
    idea = get_idea(id,)
    if request.method == 'POST':
        idea_name =request.form['idea_name']
        idea_status=request.form['idea_status']
        idea_statement =request.form['idea_statement']
        idea_issue =request.form['idea_issue']
        idea_strategy =request.form['idea_strategy']

        issue_depot =request.form['issue_depot']
        issue_driver =request.form['issue_driver']
        issue_bus =request.form['issue_bus']
        issue_trip =request.form['issue_trip']
        pitch_date =request.form['pitch_date']

        error = None

        if not idea_name:
            error = 'idea name is required.'
        
        if not idea_statement:
            error = 'idea address is required.'

        if error is not None:
            flash(error)

        else:
            db=get_db()
            db.execute(
                'UPDATE idea SET idea_name = ?, idea_status = ?,idea_statement = ?,idea_issue = ?,idea_strategy = ?,issue_depot = ?,issue_driver = ?,issue_bus = ?,issue_trip = ?,pitch_date = ?'
                ' WHERE id = ?',
                (idea_name,idea_status,idea_statement,idea_issue,idea_strategy,issue_depot,issue_bus,issue_driver,issue_trip,pitch_date,id),
            )
            db.commit()
            return redirect(url_for('dashboard.list_idea'))
    return render_template('dashboard/update_idea.html', idea=idea)

