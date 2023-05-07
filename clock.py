from apscheduler.schedulers.blocking import BlockingScheduler
from app.notifications.text_messages import next_game_sms, votes_sms, whose_playing
from rq import Queue
from worker import conn

q = Queue(connection=conn)

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='sun', hour=15, minute=20)
def next_game_text_job():
    q.enqueue(next_game_sms.send)


@sched.scheduled_job('cron', day_of_week='mon', hour=11)
def whose_playing_text_job():
    q.enqueue(whose_playing.send)


@sched.scheduled_job('cron', day_of_week='tue', hour=10)
def votes_text_job():
    q.enqueue(votes_sms.send)

sched.start()
