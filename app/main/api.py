from flask import flash, request, url_for, redirect
from flask_login import login_required
from app.schedule import next_and_prev_game
from app.auth.models.user import User
from . import api


@api.route('/record-votes', methods=['POST'])
@login_required
def record_votes():
    req = request.json
    print(req)
    flash('post votes!', category='success')
    return redirect(url_for('main.index'))
