from os import environ as env
from app import celery

@celery.task
def create_email(to, subject, body):
    # Use Celery (or something else) to implement a task queue
    from flask_mail import Message
    msg = Message('[SharksApp] ' + subject, sender=env.get("MAIL_USERNAME"), recipients=[to])
    msg.body = body
    return msg