from flask import flash, request, render_template, url_for, redirect
from flask_login import current_user, login_required
from app.schedule import next_and_prev_game
from app.auth.models.user import User
from . import api


@api.route('/votes', methods=['POST'])
@login_required
def post_votes():
    req = request.json
    flash('post votes!', category='success')
    return redirect(url_for('main.index'))


@api.route('/error-votes', methods=['GET'])
@login_required
def display_voting_error():
    flash('Voting error!', category='error')
    team = User.query.all()
    return redirect(url_for('main.votes', prev_game=next_and_prev_game.PrevGame, team=team, user=current_user))