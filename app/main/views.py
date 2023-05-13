from flask import flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import main
from ..auth.models.user import User, GameRSVP, VoteAssignment
from ..auth.models.form import RSVPForm
from app.schedule.next_and_prev_game import NextGame, PrevGame
from app import db
import json


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
    rounds_user_voted = db.session.scalars(db.select(VoteAssignment.round).filter_by(vote_giver=current_user.id)).all()
    data: Any | None = request.json
    _, round_number = data['round'].split(' ')
    round_number = int(round_number)
    if round_number in rounds_user_voted:
        flash('You have already submitted votes for this round', 'error')
    else:
        for assignment in data['assignedVotes']:
            new_assignment: VoteAssignment = VoteAssignment()
            new_assignment.season_id = data['season']
            new_assignment.round = round_number
            new_assignment.vote_giver = current_user.id
            vote_getter = db.one_or_404(db.select(User).filter_by(username=assignment['player']))
            new_assignment.vote_getter = vote_getter.id
            new_assignment.num_votes = assignment['votes']
            db.session.add(new_assignment)
            db.session.commit()

    return json.dumps({'redirect':True, 'redirectUrl': url_for('main.index')}), 302, {'ContentType':'application/json'}


@main.route('/rsvp/<round_num>', methods=['GET', 'POST'])
@login_required
def rsvp_get(round_num: str):
     form = RSVPForm
     next_round = NextGame.round
     round_text, next_round_num = next_round.split(' ')
     
     if request.method == 'GET' and next_round_num == round_num:
        return render_template('rsvp.html', user=current_user, next_game=NextGame, form=form)
     elif form.validate_on_submit():
        rsvp: GameRSVP = GameRSVP()
        rsvp.game_date = NextGame.date_str
        rsvp.user_id = current_user.id
        rsvp.is_playing = form.availability.data
        db.session.add(rsvp)
        db.session.commit()
        flash('Thanks for RSVPing -- your team mates appreciate it!', 'success')
        return json.dumps({'redirect':True, 'redirectUrl': url_for('main.index')}), 302, {'ContentType':'application/json'}
     else:
        flash('RSVP link invalid or expired', 'error')
        return redirect(url_for('main.index'))


@main.route('/my-availability', methods=['POST'])
@login_required
def rsvp_post():
    data = request.get_json() if request.is_json else None
    if not data:
        raise ValueError('No JSON data in POST request')
    

    return json.dumps({'redirect':True, 'redirectUrl': url_for('main.index')}), 302, {'ContentType':'application/json'}