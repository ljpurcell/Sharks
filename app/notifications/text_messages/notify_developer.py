from twilio.rest import Client
from app import  create_app

app = create_app("production")

def notify_developer():
    with app.app_context():
        client = Client(app.config['TWILIO_ACCOUNT_SID'],
                        app.config['TWILIO_AUTH_TOKEN'])

        message = client.messages.create(
            body="Failure to scrape schedule, check logs using heroku logs --tail",
            from_=app.config['TWILIO_PHONE_NUMBER'],
            to=app.config['MY_NUMBER']
        )



