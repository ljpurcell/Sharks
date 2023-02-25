import asyncio


def create_email(receiver_email, subject, body):
    from os import environ as env
    from flask_mail import Message
    msg = Message('[SharksApp] - ' + subject, sender=env.get("GMAIL_USERNAME"), recipients=[receiver_email])
    msg.body = body
    return msg


def create_welcome_email(user):
    subject = 'Welcome!'
    body = f'Hi {user.username},\n\nWelcome to SharksApp. Please authenticate your email by clicking the link below: LINK'
    return create_email(receiver_email=user.email, subject=subject, body=body)
    

async def send_email(email_msg):
    from app import mail
    send_mail_task = asyncio.create_task(mail.send(email_msg))
    result = await send_mail_task
    if result == 0:
        return True
    else:
        return False
    

def send_welcome_email(user):
    return send_email(create_welcome_email(user))