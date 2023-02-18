from flask import render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user
from . import main


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
    team = ["Lyndon Purcell", "Michael Walter", "Ian Johnson"] # Create get_team()
    return render_template('votes.html', prev_game=next_and_prev_game.PrevGame, team=team, total_votes=0, user=current_user)

