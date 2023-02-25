import asyncio
from app import mail
from os import environ as env
from flask_mail import Message


def create_email(receiver_email, subject, body):
    msg = Message('[SharksApp] - ' + subject, sender=env.get("GMAIL_USERNAME"), recipients=[receiver_email])
    msg.body = body
    return msg


def create_welcome_email(user):
    subject = 'Welcome!'
    body = f'Hi {user.username},\n\nWelcome to SharksApp. Please authenticate your email by clicking the link below: LINK'
    return create_email(receiver_email=user.email, subject=subject, body=body)
    

def send_email(email_msg):
    mail.send(email_msg)
    

def send_welcome_email(user):
    send_email(create_welcome_email(user))