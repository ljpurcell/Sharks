from flask import current_app as app
from twilio.rest import Client
from app.auth.models.user import User, GameRSVP
from app.schedule.next_and_prev_game import NextGame
import json


client: Client = Client(
    app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

team_members: list[User] = db.session.execute(db.select(User)).all()
confirmed_playing: list[User] = db.session.execute(
    db.select(GameRSVP)).filter_by(date_str=NextGame.date_str, is_playing=True)
confirmed_out: list[User] = db.session.execute(db.select(GameRSVP)).filter_by(
    date_str=NextGame.date_str, is_playing=False)

message_body: str = "Playing: " + \
    json.dumps(confirmed_playing) + "\n\nNot playing: " + \
    json.dumps(confirmed_out)

if not NextGame.is_bye:
    for team_member in team_members:
        message = client.messages.create(
            body=message_body,
            from_=app.config['TWILIO_PHONE_NUMBER'],
            to=team_member.mobile
        )
