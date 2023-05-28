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
        day, date = NextGame.date_str.split(' ')

        playing_query = db.select(User.username).join(GameRSVP, User.id==GameRSVP.user_id).where(GameRSVP.game_date==date).where(GameRSVP.is_playing==True)
        
        print(playing_query)
        playing_users = db.session.execute(playing_query)

        out_users = db.session.execute(
            db.select(User.username)
            .join(GameRSVP, User.id==GameRSVP.user_id)
            .where(GameRSVP.game_date==GameRSVP.game_date==date)
            .where(GameRSVP.is_playing==False))
    

        message_body: str = "Playing: " + playing_users + "\n\nNot playing: " + out_users

        if not NextGame.is_bye:
            for team_member in team_members:
                if team_member.username == "Lyndon":
                    message = client.messages.create(
                        body=message_body,
                        from_=app.config['TWILIO_PHONE_NUMBER'],
                        to=team_member.mobile
                    ) 
