from flask import flash, request, url_for, redirect
from flask_login import login_required
from app.schedule import next_and_prev_game
from app.auth.models.user import User
from . import api
import json


@api.route('/record-votes', methods=['POST'])
@login_required
def record_votes():
    data = request.json
    print(data)
    # TODO Create new vote assignment for each in array
    for assignment in data['assignedVotes']:
        # season_id
        # round
        # vote giver
        # vote getter
        # number of votes

    return json.dumps({'redirect':True, 'redirectUrl': url_for('main.index')}), 302, {'ContentType':'application/json'}
