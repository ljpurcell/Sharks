from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import main
from ..auth.models.user import User, GameRSVP, VoteAssignment
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

@main.route('/record-votes', methods=['POST'])
@login_required
def record_votes():
    data: Any | None = request.json
    for assignment in data['assignedVotes']:
        new_assignment: VoteAssignment = VoteAssignment()
        new_assignment.season_id = data['season']
        new_assignment.round = data['round']
        new_assignment.vote_giver = current_user.id
        vote_getter = db.one_or_404(db.select(User).filter_by(username=assignment['player']))
        new_assignment.vote_getter = vote_getter.id
        new_assignment.num_votes = assignment['votes']
        db.session.add(new_assignment)
        db.session.commit()

    return json.dumps({'redirect':True, 'redirectUrl': url_for('main.index')}), 302, {'ContentType':'application/json'}


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

