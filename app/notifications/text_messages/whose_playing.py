from datetime import datetime
now = datetime.now()

# Sunday (6) at 5pm (7am UTC)
if now.weekday() == 6 and now.hour == 7 or True:
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

        playing_query = db.select(User).join(GameRSVP, User.id==GameRSVP.user_id).where(GameRSVP.game_date==NextGame.date_str).where(GameRSVP.is_playing==True)
        
        print(playing_query)
        playing_users: list[User] = db.session.execute(playing_query)

        out_users: list[User] = db.session.execute(
            db.select(User.username)
            .join(GameRSVP, User.id==GameRSVP.user_id)
            .where(GameRSVP.game_date==NextGame.date_str)
            .where(GameRSVP.is_playing==False))
        
        confirmed_playing = []
        confirmed_out = []

        for user in playing_users:
            confirmed_playing.append(user.username)

        for user in out_users:
            confirmed_out.append(user.username)

        message_body: str = "Playing: " + json.dumps(confirmed_playing) + "\n\nNot playing: " + json.dumps(confirmed_out)

        if not NextGame.is_bye:
            for team_member in team_members:
                if team_member.username == "Lyndon":
                    message = client.messages.create(
                        body=message_body,
                        from_=app.config['TWILIO_PHONE_NUMBER'],
                        to=team_member.mobile
                    ) 
