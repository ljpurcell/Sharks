from crontab import CronTab

cron = CronTab(user='LJPurcell')
cron.remove_all() # Be careful to remove in the future

schedule_game_text = cron.new(command='/Users/LJPurcell/Code/Sharks/venv/bin/python3 /Users/LJPurcell/Code/Sharks/app/next_game_sms.py', comment="Next game text")
schedule_game_text.setall('0 18 * * SUN')

schedule_votes_text = cron.new(command='/Users/LJPurcell/Code/Sharks/venv/bin/python3 /Users/LJPurcell/Code/Sharks/app/votes_sms.py', comment="Votes text")
schedule_votes_text.setall('0 10 * * TUE')

cron.write()