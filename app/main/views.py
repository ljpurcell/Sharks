from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import logging
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
    team: list[User] = db.session.scalars(db.select(User)).all()
    return render_template('votes.html', prev_game=PrevGame, team=team, user=current_user)


@main.route('/rsvp/<token>', methods=['GET', 'POST'])
@login_required
def rsvp(token: str):
    response: str = current_user.confirm_rsvp_token(token)
    id, date = response.split(',')
    id = int(id)

    if (request.method == 'GET') and (current_user.id == id) and (NextGame.date_str == date):
        flash('Token valid. Please confirm whether or not you are playing!', 'success')
        return render_template('rsvp.html', user=current_user, token=token, next_game=NextGame)
    
    elif request.method == 'POST' and (current_user.id == id) and (NextGame.date_str == date):
        logging.debug('Request: ' + request)
        logging.debug('Request is_json: ' + request.is_json)
        logging.debug('Request get_json(): ' + request.get_json())
        logging.debug('Request json(): ' + request.json())
        data = request.get_json() if request.is_json else None
        if not data:
            raise ValueError('No JSON data in POST request')
        availability = data['availability']
        rsvp: GameRSVP = GameRSVP()
        rsvp.game_date = date
        rsvp.user_id = id
        rsvp.is_playing = availability
        db.session.add(rsvp)
        db.session.commit()
        flash('Thanks for RSVPing -- your team mates appreciate it!', 'success')

    else:
        flash('RSVP link invalid or expired', 'error')
        
    return redirect(url_for('main.index'))

