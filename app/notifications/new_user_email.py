from celery import Celery

celery = Celery('new_user_email', broker='amqp://localhost:5000')

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
    

def send_email(email_msg):
    from app import mail
    result = mail.send(email_msg)
    if result == 0:
        return True
    else:
        return False
    
@celery.task
def send_welcome_email(user):
    from os import system
    system.run('echo we got here')
    return send_email(create_welcome_email(user))