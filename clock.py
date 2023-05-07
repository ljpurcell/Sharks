from apscheduler.schedulers.blocking import BlockingScheduler
from app.notifications.text_messages import next_game_sms, votes_sms, whose_playing

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='sun', hour=15)
def next_game_text_job():
    next_game_sms.send()


@sched.scheduled_job('cron', day_of_week='mon', hour=11)
def whose_playing_text_job():
    whose_playing.send()


@sched.scheduled_job('cron', day_of_week='tue', hour=10)
def votes_text_job():
    votes_sms.send()

sched.start()
