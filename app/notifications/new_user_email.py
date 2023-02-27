from app import mail, celery
from os import environ as env
from flask_mail import Message
from ..auth.models.user import User


def create_email(receiver_email, subject, body):
    msg = Message('[SharksApp] - ' + subject, sender=env.get("GMAIL_USERNAME"), recipients=[receiver_email])
    msg.body = body
    return msg


def create_welcome_email(user):
    subject = 'Welcome!'
    body = f'Hi {user.username},\n\nWelcome to SharksApp. Please authenticate your email by clicking the link below: LINK'
    return create_email(receiver_email=user.email, subject=subject, body=body)

    

def send_welcome_email(user_id):
    send_async_welcome_email.delay(user_id)


@celery.task
def send_async_welcome_email(user_id):
    user = User.query.get(int(user_id))
    email_msg = create_welcome_email(user)
    print(celery.conf)
    mail.send(email_msg)