from crontab import CronTab

cron = CronTab(user='LJPurcell')

schedule_text = cron.new(command='/Users/LJPurcell/Code/Sharks/venv/bin/python3 /Users/LJPurcell/Code/Sharks/app/text_message.py')
schedule_text.setall('0 12 * * 2')

cron.write()