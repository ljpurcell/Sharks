from datetime import datetime
now = datetime.now()

# Sunday (6) at 5pm (7am UTC)
if now.weekday() == 6 and now.hour == 7:
    from twilio.rest import Client
    from app.auth.models.user import User, GameRSVP
    from app.schedule.next_and_prev_game import NextGame
    import json
    from app import db, create_app

    app = create_app("production")
    
    with app.app_context():
        client: Client = Client(
            app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

        team_members: list[User] = db.session.scalars(db.select(User)).all()

        confirmed_playing: list[str] = db.session.scalars(
            db.select(User.username)
            .join(GameRSVP, User.id==GameRSVP.user_id)
            .filter_by(game_date=NextGame.date_str, is_playing=True)).all() # TODO 
         

        confirmed_out: list[str] = db.session.scalars(
            db.select(User.username)
            .join(GameRSVP, User.id==GameRSVP.user_id)
            .filter_by(game_date=NextGame.date_str, is_playing=False)).all() # TODO 

        message_body: str = "Playing: " 
        #+ json.dumps(confirmed_playing) + "\n\nNot playing: " + json.dumps(confirmed_out)

        if not NextGame.is_bye:
            for team_member in team_members:
                if team_member.username == "Lyndon":
                    message = client.messages.create(
                        body=message_body,
                        from_=app.config['TWILIO_PHONE_NUMBER'],
                        to=team_member.mobile
                    ) 
