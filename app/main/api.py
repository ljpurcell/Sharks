from flask import flash, request, render_template, get_flashed_messages, redirect
from flask_login import current_user, login_required
from app.schedule import next_and_prev_game
from app.auth.models.user import User
import json
from . import api


@api.route('/votes', methods=['POST'])
@login_required
def post_votes():
    req = request.json
    flash('post votes!', category='success')
    team = User.query.all()
    return render_template('votes.html', prev_game=next_and_prev_game.PrevGame, team=team, user=current_user)


@api.route('/error-votes', methods=['POST'])
@login_required
def display_voting_error():
    flash('Voting error!', category='success')
    m = get_flashed_messages()
    print(m)
    team = User.query.all()
    return render_template('votes.html', prev_game=next_and_prev_game.PrevGame, team=team, user=current_user)