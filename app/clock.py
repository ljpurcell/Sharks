from crontab import CronTab

cron = CronTab(user='LJPurcell')
cron.remove_all() # Be careful to remove in the future

schedule_game_text = cron.new(command='/Users/LJPurcell/Code/Sharks/prod/bin/python3 /Users/LJPurcell/Code/Sharks/app/notifications/text_messages/next_game_sms.py', comment="Next game text")
schedule_game_text.setall('0 18 * * SUN')

schedule_game_text = cron.new(command='/Users/LJPurcell/Code/Sharks/prod/bin/python3 /Users/LJPurcell/Code/Sharks/app/notifications/text_messages/whose_playing.py', comment="Whose playing text")
schedule_game_text.setall('0 12 * * MON')

schedule_votes_text = cron.new(command='/Users/LJPurcell/Code/Sharks/prod/bin/python3 /Users/LJPurcell/Code/Sharks/app/notifications/text_messages/votes_sms.py', comment="Votes text")
schedule_votes_text.setall('0 10 * * TUE')

cron.write()