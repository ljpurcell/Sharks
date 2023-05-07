from datetime import datetime
now = datetime.now()

print("got here")
if now.weekday() == 6 and now.hour == 16:
    ("and here")
    from app.schedule.next_and_prev_game import NextGame
    from flask import current_app as app
    from app.auth.models.user import User
    from twilio.rest import Client
    from app import db
    from app.schedule.game import Game


    client = Client(app.config['TWILIO_ACCOUNT_SID'],
                    app.config['TWILIO_AUTH_TOKEN'])


    def generate_message_body(next_game: Game, user: User) -> str:
        if next_game is None:
            message_body = "Well done on the season -- thanks for being a part of this cut-throat unit... Got the whole world is looking like shark bait at the minute!\n\nBe sure to rest up and hit the practice court in the off-season.\n\nStay tuned for Sharks Brownlow."
        elif next_game.is_bye:
            message_body = next_game.round + " - " + \
                next_game.date_str + "\n\n" + next_game.teams
        else:
            message_body = next_game.round + " - " + next_game.date_str + "\n\n" + next_game.teams + "\n\n" + next_game.time_str + \
                " at " + next_game.location + \
                ".\n\nClick this link (24H only) to RSVP: " + \
                user.generate_rsvp_token(next_game.date_str)
        return message_body


    team_members: list[User] = db.session.scalars(db.select(User)).all()

    for team_member in team_members:
        message = client.messages.create(
            body=generate_message_body(NextGame, team_member),
            from_=app.config['TWILIO_PHONE_NUMBER'],
            to=team_member.mobile
        )
