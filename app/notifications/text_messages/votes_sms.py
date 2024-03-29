from datetime import datetime
from zoneinfo import ZoneInfo

melb_timezone = ZoneInfo("Australia/Melbourne") 
now = datetime.now(tz=melb_timezone)

# Tuesday at 11am 
if now.weekday() == 1 and now.time == 11:
    from twilio.rest import Client
    from os import environ as env
    from app.auth.models.user import User
    from app import db, create_app
    from app.schedule.next_and_prev_game import PrevGame

    app = create_app("production")
    
    with app.app_context():
        client: Client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

        team_members: list[User] = db.session.scalars(db.select(User)).all()

        message_body: str = "Get those votes in!\n\n" + app.config['APP_URL'] + "/votes"

        if not PrevGame.is_bye:
            for team_member in team_members:
                message = client.messages.create(
                    body=message_body,
                    from_=app.config['TWILIO_PHONE_NUMBER'],
                    to=team_member.mobile
                )
