from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import main
from ..auth.models.user import User, GameRSVP
from app.schedule.next_and_prev_game import NextGame, PrevGame
from app import db


@main.route('/')
def index():
    return render_template('index.html', user=current_user)

@main.route('/next-game', methods=['GET'])
@login_required
def next_game():
    return render_template('next.html', next_game=NextGame, user=current_user)

@main.route('/votes')
@login_required
def votes():
    team = User.query.all()
    return render_template('votes.html', prev_game=PrevGame, team=team, user=current_user)


@main.route('/rsvp/<token>', methods=['GET', 'POST'])
@login_required
def rsvp(token):
    response = current_user.confirm_rsvp_token(token)

    if request.method == 'GET' and response == [current_user.id, NextGame.date_str]:
        flash('Token valid. Please confirm whether or not you are playing!', 'success')
        return render_template('rsvp.html', user=current_user, token=token, next_game=NextGame)
    
    elif request.method == 'POST' and response == [current_user.id, NextGame.date_str]:
        rsvp = GameRSVP()
        rsvp.game_date = response[1]
        rsvp.user_id = response[0]
        db.session.add(rsvp)
        db.session.commit()
        flash('Thanks for RSVPing -- your team mates appreciate it!', 'success')

    else:
        flash('RSVP link invalid or expired', 'error')
        
    return redirect(url_for('main.index'))

