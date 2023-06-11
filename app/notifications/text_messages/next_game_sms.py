from datetime import datetime
now = datetime.now()

# Sunday (6) at 11am (1am UTC)
if now.weekday() == 6 and now.hour == 1:
    from app.schedule.next_and_prev_game import NextGame
    from app.auth.models.user import User
    from twilio.rest import Client
    from app import db, create_app
    from app.schedule.game import Game

    app = create_app("production")

    def generate_message_body(next_game: Game, app) -> str:
        if next_game is None:
            message_body = "Well done on the season -- thanks for being a part of this cut-throat unit... Got the whole world looking like shark bait at the minute!\n\nBe sure to rest up and hit the practice court in the off-season.\n\nStay tuned for Sharks Brownlow."
        elif next_game.is_bye:
            message_body = next_game.round + " - " + \
                next_game.date_str + "\n\n" + next_game.teams
        else:
            round_label, round_num = next_game.round.split(' ')
            message_body = next_game.round + " - " + next_game.date_str + "\n\n" + next_game.teams + "\n\n" + next_game.time_str + \
                " at " + next_game.location + \
                ".\n\nClick this link to RSVP: " + app.config['APP_URL'] + "/rsvp/" + round_num
        return message_body

    with app.app_context():
        client = Client(app.config['TWILIO_ACCOUNT_SID'],
                        app.config['TWILIO_AUTH_TOKEN'])

        team_members: list[User] = db.session.scalars(db.select(User)).all()
        
        for team_member in team_members:
            message = client.messages.create(
                body=generate_message_body(NextGame, app),
                from_=app.config['TWILIO_PHONE_NUMBER'],
                to=team_member.mobile
            )
