from flask import current_app as app
from twilio.rest import Client
from os import sys

sys.path.append('/Users/LJPurcell/Code/Sharks/app/schedule')

from app.schedule.next_and_prev_game import PrevGame

client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

team_members = [
  "+61447915198", # Me
  "+61447615707", # Walt
  "+61488920388", # AJ    
  "+61427987353", # IJ
  "+61429867267", # Reece
  "+61407506565", # Vin
  "+61447744628", # Nick
]

message_body = "Get those votes in!\n\nhttps://docs.google.com/forms/d/e/1FAIpQLSfl8KvtJUJI4OYB1BWCCDV1Hj3Dspe6X21qPVcOOL60eFny6A/viewform"

if not PrevGame.is_bye:
    for team_member in team_members:
        message = client.messages.create(
            body=message_body,
            from_=app.config['TWILIO_PHONE_NUMBER'],
            to=team_member
        )
