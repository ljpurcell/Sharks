from flask import current_app as app
from app.auth.models.user import User
from twilio.rest import Client


client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

from app.schedule.next_and_prev_game import NextGame

def generate_message_body(next_game, user):
  if next_game is None:
    message_body = "Well done on the season. The whole world is looking like shark bait at the minute\n\nBe sure to rest up and hit the practice court in the off-season.\n\nStay tuned for Sharks Brownlow."
  elif next_game.is_bye:
    message_body = next_game.round + " - " + next_game.date_str + "\n\n" + next_game.teams
  else:
    message_body = next_game.round + " - " + next_game.date_str + "\n\n" + next_game.teams + "\n\n" + next_game.time_str + " at " + next_game.location + ".\n\nClick this link (24H only) to RSVP: " + user.generate_rsvp_token(next_game.date_str)
  return message_body


# TODO query db for all users
team_members = User.query.all()

for team_member in team_members:
  message = client.messages.create(
    body=generate_message_body(NextGame, team_member),
    from_=app.config['TWILIO_PHONE_NUMBER'],
    to=team_member.mobile
  )