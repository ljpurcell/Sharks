from os import environ as env
from flask_mail import Message
from . import celery, mail
from .auth.models.user import User



@celery.task(name='send_async_welcome_email')
def send_async_welcome_email(user_id):
    user = User.query.get(int(user_id))
    email_msg = create_welcome_email(user)
    print(celery.conf)
    mail.send(email_msg)


def create_welcome_email(user):
    msg = Message('[SharksApp] - Welcome', sender=env.get("GMAIL_USERNAME"), recipients=[user.email])
    msg.subject = 'Welcome!'
    msg.body = f'Hi {user.username},\n\nWelcome to SharksApp. Please authenticate your email by clicking the link below: LINK'
    return msg
    

def send_welcome_email(user_id):
    send_async_welcome_email.delay(user_id)