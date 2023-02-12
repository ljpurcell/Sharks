from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/next-game', methods=['GET'])
def next_game():
    from ..next_and_prev_game import NextGame
    return render_template('next.html', next_game=NextGame)

@main.route('/votes')
def votes():
    from ..next_and_prev_game import PrevGame
    team = ["Lyndon Purcell", "Michael Walter", "Ian Johnson"] # Create get_team()
    return render_template('votes.html', prev_game=PrevGame, team=team, total_votes=0)

