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

#################################################################################### [PAGE MAIN]

@bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')
#################################################################################### [HOSTING MAIN]

@bp.route('/hosting')
@login_required
def hosting():
    return render_template('dashboard/hosting.html')

#################################################################################### [SHOW HOSTING]

@bp.route('/list_hosting')
@login_required
def list_hosting():
    db = get_db()
    todos = db.execute(
        'SELECT id, todo_owner, task_name, task_description, due_date, status'
        ' FROM todos'
        ' WHERE todo_owner = ?',(g.user['username'],)
        #' ORDER BY id ASC'
    ).fetchall()
    return render_template('dashboard/list_hosting.html', todos=todos)

####################################################################################

def get_task(id):
    task = get_db().execute(
        'SELECT id, todo_owner, task_name, task_description, due_date, status'
        ' FROM todos'
        ' WHERE id = ?',(id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    return task

#################################################################################### [UPDATE HOSTING]

@bp.route('/<int:id>/update_hosting', methods=('GET', 'POST'))
@login_required
def update_hosting(id):
    todos = get_task(id,)

    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        status = request.form['status']
        error = None

        if not task_name:
            error = 'Task name is required.'
        
        if not task_description:
            error = 'Task description is required.'

        if not due_date:
            error = 'Due date is required.'
        
        if not status:
            error = 'Status is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE todos SET task_name = ?, task_description = ?, due_date = ?, status = ?'
                ' WHERE id = ?',
                (task_name, task_description, due_date, status, id)
            )
            db.commit()
            return redirect(url_for('dashboard.list_hosting'))

    return render_template('dashboard/update_hosting.html', todos=todos)

#################################################################################### [DELETE HOSTING]

@bp.route('/<int:id>/delete_hosting', methods=('POST',))
@login_required
def delete_hosting(id):
    get_task(id,)
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard.list_hosting'))




#################################################################################### [ADD PROPERTY]

@bp.route('/add_property', methods = ['POST','GET'])
@login_required
def add_property():
    if request.method == 'POST':
        property_name =request.form['property_name']
        property_status=request.form['property_status']
        property_address =request.form['property_address']
        stateInput =request.form['stateInput']
        districtInput =request.form['districtInput']
        ttl_room =request.form['ttl_room']
        ttl_bathroom =request.form['ttl_bathroom']
        aircond =request.form['aircond']
        wifi =request.form['wifi']
        washing =request.form['washing']
        cooking =request.form['cooking']
        homestay_rate =request.form['homestay_rate']
        phone =request.form['phone']
        error = None

        if not property_name:
            error = 'Property name is required.'
        elif not property_address:
            error = 'Property address is required.'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                "INSERT INTO property (property_name,property_status,property_address,stateInput,districtInput,ttl_room,ttl_bathroom,aircond,wifi,washing,cooking,homestay_rate,phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (property_name, property_status, property_address, stateInput, districtInput, ttl_room, ttl_bathroom, aircond, wifi, washing, cooking, homestay_rate, phone),
            )
            db.commit()
            return redirect(url_for('dashboard.list_property'))
    return render_template('dashboard/add_property.html')

#################################################################################### [DELETE PROPERTY]

@bp.route('/<int:id>/delete_property', methods=('POST',))
@login_required
def delete_property(id):
    get_task(id,)
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard.list_property'))

#################################################################################### [LIST PROPERTY]

@bp.route('/list_property')
@login_required
def list_property():
    db = get_db()
    properties = db.execute(
        'SELECT id,property_name,property_status,property_address,stateInput,districtInput,ttl_room,ttl_bathroom,aircond,wifi,washing,cooking,homestay_rate,phone'
        ' FROM property'
        ' WHERE phone = ?',(g.user['phone'],)
        #' ORDER BY id ASC'
    ).fetchall()
    return render_template('dashboard/list_property.html', properties=properties)

####################################################################################

def get_property(id):
    property = get_db().execute(
        'SELECT id,property_name,property_status,property_address,stateInput,districtInput,ttl_room,ttl_bathroom,aircond,wifi,washing,cooking,homestay_rate,phone'
        ' FROM property'
        ' WHERE id = ?',(id,)
    ).fetchone()

    if property is None:
        abort(404, f"Property id {id} doesn't exist.")

    return property

#################################################################################### [UPDATE PROPERTY]

@bp.route('/<int:id>/update_property', methods=('GET', 'POST'))
@login_required
def update_property(id):
    property = get_property(id,)
    if request.method == 'POST':
        property_name =request.form['property_name']
        property_address =request.form['property_address']
        stateInput =request.form['stateInput']
        districtInput =request.form['districtInput']
        ttl_room =request.form['ttl_room']
        ttl_bathroom =request.form['ttl_bathroom']
        aircond =request.form['aircond']
        wifi =request.form['wifi']
        washing =request.form['washing']
        cooking =request.form['cooking']
        homestay_rate =request.form['homestay_rate']
        error = None

        if not property_name:
            error = 'Property name is required.'
        
        if not property_address:
            error = 'Property address is required.'

        if error is not None:
            flash(error)

        else:
            db=get_db()
            db.execute(
                'UPDATE property SET property_name = ?, property_address = ?,stateInput = ?,districtInput = ?,ttl_room = ?,ttl_bathroom = ?,aircond = ?,wifi = ?,washing = ?,cooking = ?,homestay_rate = ?'
                ' WHERE id = ?',
                (property_name, property_address, stateInput, districtInput, ttl_room, ttl_bathroom, aircond, wifi, washing, cooking, homestay_rate, id),
            )
            db.commit()
            return redirect(url_for('dashboard.list_property'))
    return render_template('dashboard/update_property.html', property=property)

#################################################################################### [GUEST SEARCH]

@bp.route('/search_property', methods=('GET', 'POST'))
@login_required
def search_property():
    if request.method == 'POST':
        stateInput =request.form['stateInput']
        districtInput =request.form['districtInput']
        ttl_room =request.form['ttl_room']
        ttl_bathroom =request.form['ttl_bathroom']
        aircond =request.form['aircond']
        wifi =request.form['wifi']
        washing =request.form['washing']
        cooking =request.form['cooking']
        homestay_rate =request.form['homestay_rate']

        error = None

        if not stateInput:
            error = 'State name is required.'
        
        if not districtInput:
            error = 'District name is required.'

        if not ttl_room:
            error = 'District name is required.'
        
        if not ttl_bathroom:
            error = 'District name is required.'

        if not aircond:
            error = 'State name is required.'
        
        if not wifi:
            error = 'District name is required.'

        if not washing:
            error = 'District name is required.'
        
        if not cooking:
            error = 'District name is required.'

        if not homestay_rate:
            error = 'District name is required.'

        if error is not None:
            flash(error)

    return render_template('dashboard/search_property.html')

#################################################################################### [GUEST BOOKING]
'''
@bp.route('/book_property', methods = ['POST','GET'])
@login_required
def book_property():
    db = get_db()
    properties = db.execute(
        'SELECT id,property_name,property_status,property_address,stateInput,districtInput,ttl_room,ttl_bathroom,aircond,wifi,washing,cooking,homestay_rate,phone'
        ' FROM property'
        #' ORDER BY id ASC'
    ).fetchall()
    return render_template('dashboard/book_property.html', properties=properties)
'''
#################################################################################### [TRAVELLING MAIN]

@bp.route('/travelling')
@login_required
def travelling():
    return render_template('dashboard/travelling.html')
