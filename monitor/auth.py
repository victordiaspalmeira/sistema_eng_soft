import functools
import os,sys,inspect

import sqlite3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return 'NO USER'
        else:
            return 'USER'

    return wrapped_view

@bp.route('/register_user', methods=('GET', 'POST'))
def register_user():
    conn = sqlite3.connect('engsoft.db')
    c = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        INST_ID = request.form['INST_ID']
        INST_TYPE = request.form['INST_TYPE']
        NOME = request.form['NOME']
        SOBRENOME = request.form['SOBRENOME']
        CARGO = request.form['CARGO']
        EMAIL =  request.form['EMAIL']
        TELEFONE = request.form['TELEFONE']

        error = None

        if not username:
            error = "USERNAME MISSING"
        elif not password:
            error = 'PASSWORD MISSING'
        elif not INST_ID:
            error = 'INST_ID MISSING'
        elif not INST_TYPE:
            error = 'INST_TYPE MISSING'
        elif not NOME:
            error ='NOME MISSING'
        elif not SOBRENOME:
            error ='SOBRENOME MISSING'
        elif not CARGO:
            error ='CARGO MISSING'
        elif not EMAIL:
            error = 'EMAIL MISSING'
        elif not TELEFONE:
            error = 'TELEFONE MISSING'
        else:
            try:
                c.execute(f"SELECT id FROM USER WHERE username = '{username}'").fetchone()
                c.fetchall()
                error = 'USER ALREADY EXISTS'
            except Exception as e:
                return str(e)

        if error is None:
            print(username, password)
            try:
                sql =  f"INSERT INTO user (INST_ID, INST_TYPE, username, password, NOME, SOBRENOME, CARGO, EMAIL, TELEFONE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                val = (INST_ID, INST_TYPE, username, generate_password_hash(password), NOME, SOBRENOME, CARGO, EMAIL, TELEFONE)
                c.execute(sql, val)
                conn.commit()
                session['user-id'] = username
                print(val)
                conn.close()
                return 'REGISTER SUCCESSFUL\n'+str(val)
            except Exception as e:
                return str(e)
    else:
        error = 'BAD REGISTER'
    return error

@bp.route('/test', methods=('GET', 'POST'))
@login_required
def test():
    return 'GOOD'

@bp.route('/register_inst', methods=('GET', 'POST'))
@login_required
def register_inst():
    conn = sqlite3.connect('engsoft.db')
    c = conn.cursor()    
    if request.method == 'POST':
        NOME = request.form['NOME']
        VISIVEL = request.form['VISIVEL']
        ENDERECO = request.form['ENDERECO']
        CIDADE =  request.form['CIDADE']
        ESTADO = request.form['ESTADO']
        MANTENEDORA = request.form['MANTENEDORA']

        if not NOME:
            error ='NOME MISSING'
        elif not VISIVEL:
            error = 'VISIVEL MISSING'
        elif not ENDERECO:
            error = 'ENDERECO MISSING'
        elif not CIDADE:
            error = 'CIDADE MISSING'
        elif not ESTADO:
            error = 'ESTADO MISSING'
        elif not CREDENCIAMENTO:
            error = 'CREDENCIAMENTO MISSING'
        elif not MANTENEDORA:
            error = 'MANTENEDORA MISSING'           
        else:
            try:
                c.execute(f"SELECT id FROM INST WHERE NOME = '{NOME}'").fetchone()
                c.fetchall()
                error = 'INST ALREADY EXISTS'
            except:
                pass
    return 'INST OK'

@bp.route('/login', methods=('GET', 'POST'))
def login():
    conn = sqlite3.connect('engsoft.db')
    c = conn.cursor()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        sql = f"SELECT * FROM USER WHERE username = '{username}'"
        c.execute(sql)
        user = c.fetchone()
        print('USER', user)
        if user is None:
            error = 'USER ERROR'
        elif not check_password_hash(user[4], password):
            error = 'PASSWORD ERROR'

        if error is None:
            #print("No error")
            session.clear()
            session['user_id'] = user[0]
            return 'LOGIN SUCCESSFUL'
    else:
        error = 'BAD LOGIN'

    return error

@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print('=============', g.__dict__)
    if user_id is None:
        g.user = None
    else:
        conn = sqlite3.connect('engsoft.db')
        c = conn.cursor()
        command = f"SELECT * FROM USER WHERE id = '{user_id}'"
        try:
            c.execute(command)
        except Exception as e:
            print(e)
            return 'BAD LOGIN '+str(e)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



