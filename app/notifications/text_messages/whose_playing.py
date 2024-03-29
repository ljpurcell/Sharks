from datetime import datetime
from zoneinfo import ZoneInfo

melb_timezone = ZoneInfo("Australia/Melbourne") 
now = datetime.now(tz=melb_timezone)


# Sunday at 5pm 
if now.weekday() == 6 and now.hour == 17:
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
        
        playing_users = db.session.execute(
            db.select(User.username)
            .join(GameRSVP, User.id==GameRSVP.user_id)
            .where(GameRSVP.game_date==date)
            .where(GameRSVP.is_playing==True)).all()

        out_users = db.session.scalars(
            db.select(User.username)
            .join(GameRSVP, User.id==GameRSVP.user_id)
            .where(GameRSVP.game_date==GameRSVP.game_date==date)
            .where(GameRSVP.is_playing==False)).all()
    
        playing_users = [user[0] for user in playing_users]
        out_users = [user[0] for user in out_users]

        message_body: str = "Confirmed playing: " + json.dumps(playing_users) + "\n\nConfirmed out: " + json.dumps(out_users)

        if not NextGame.is_bye:
            for team_member in team_members:
                message = client.messages.create(
                    body=message_body,
                    from_=app.config['TWILIO_PHONE_NUMBER'],
                    to=team_member.mobile
                ) 
