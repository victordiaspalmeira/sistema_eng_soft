import flask
import sqlite3
from sqlite3_manager import create_connection, get_user
from werkzeug.security import check_password_hash, generate_password_hash
app = flask.Flask(__name__)
app.config["DEBUG"] = True

from flask import (
    request
)

#LOGIN
@app.route('/login', methods=('GET','POST'))
def login():
    username = request.form['username']
    password = request.form['password']
    error = None
    if not username:
        error = 'USERNAME MISSING'
    elif not password:
        error = 'PASSWORD MISSING'

    if error is None:
        conn = create_connection('engsoft.db')
        conn.row_factory = sqlite3.Row
        cursor()
        command = f"SELECT * FROM users WHERE username = '{username}'"
        c.execute(command)
        user = get_user

        if user is None:
            error = 'INCORRECT USERNAME'
        elif not check_password_has(user['password'], password):
            error = 'INCORRECT PASSWORD'

    if error is None:
        return {'id': user['id'], 'cargo': user['cargo']}
    

app.run(debug=False)