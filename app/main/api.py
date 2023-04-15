from flask import flash, request, url_for, redirect
from flask_login import login_required, current_user
from app.auth.models.user import User, VoteAssignment
from . import api
from app import db
import json


@api.route('/record-votes', methods=['POST'])
@login_required
def record_votes():
    data = request.json
    print(data)
    print(current_user.id)
    for assignment in data['assignedVotes']:
        new_assignment = VoteAssignment()
        new_assignment.season_id = data['season']
        new_assignment.round = data['round']
        new_assignment.vote_giver = current_user.id
        vote_getter = User.query.filter_by(username=assignment['player']).first()
        new_assignment.vote_getter = vote_getter.id
        new_assignment.num_votes = assignment['votes']
        db.session.add(new_assignment)
        db.session.commit()

    return json.dumps({'redirect':True, 'redirectUrl': url_for('main.index')}), 302, {'ContentType':'application/json'}
