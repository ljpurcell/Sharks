from crontab import CronTab

cron = CronTab(user='LJPurcell')
cron.remove_all() # Be careful to remove in the future

schedule_text = cron.new(command='/Users/LJPurcell/Code/Sharks/venv/bin/python3 /Users/LJPurcell/Code/Sharks/app/text_message.py', comment="Next game notification")
schedule_text.setall('0 18 * * SUN')

cron.write()