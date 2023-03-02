from flask import flash, render_template
from flask_login import login_required, current_user
from . import main
from ..auth.models.user import User


@main.route('/')
def index():
    return render_template('index.html', user=current_user)


@main.route('/next-game', methods=['GET'])
@login_required
def next_game():
    from app.schedule.next_and_prev_game import NextGame
    return render_template('next.html', next_game=NextGame, user=current_user)

@main.route('/votes')
@login_required
def votes():
    from app.schedule import next_and_prev_game
    team = User.query.all()
    return render_template('votes.html', prev_game=next_and_prev_game.PrevGame, team=team, user=current_user)

