from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from monitor.auth import login_required

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    command = 'SELECT * from modelInfo'
    cursor.execute(command)
    rows = cursor.fetchall()
    dev_ids = list()
    for row in rows:
        dev_ids.append(row['dev_id'])
        print(row['dev_id'])
    return render_template('index/index.html', dev_ids=dev_ids)