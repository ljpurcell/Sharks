from flask import current_app as app
from twilio.rest import Client


client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

from app.schedule.next_and_prev_game import NextGame

if NextGame is None:
  message_body = "No more games. Try suspend Twilio and erase cronjob running script. Prepare code for next season"
elif NextGame.is_bye:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n\n" + NextGame.teams
else:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n\n" + NextGame.teams + "\n\n" + NextGame.time_str + " at " + NextGame.location


team_members = [
  "+61447915198", # Me
  "+61447615707", # Walt
  "+61488920388", # AJ    
  "+61427987353", # IJ
  "+61429867267", # Reece
  "+61407506565", # Vin
  "+61447744628", # Nick
]
if NextGame is None:
  message = client.messages.create(
    body=message_body,
    from_=app.config['TWILIO_PHONE_NUMBER'],
    to=app.config['MY_NUMBER']
  )
else:
  for team_member in team_members:
    message = client.messages.create(
      body=message_body,
      from_=app.config['TWILIO_PHONE_NUMBER'],
      to=team_member
    )