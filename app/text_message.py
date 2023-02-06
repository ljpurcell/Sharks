from os import environ as env
from os.path import join
from twilio.rest import Client
from dotenv import load_dotenv

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = join('/Users/LJPurcell/Code/Sharks/.env')
load_dotenv(dotenv_path=dotenv_path)

client = Client(env["TWILIO_ACCOUNT_SID"], env["TWILIO_AUTH_TOKEN"])

from next_and_prev_game import NextGame

if NextGame is None:
  message_body = "No more games. Try suspend Twilio and erase cronjob running script. Prepare code for next season"
elif NextGame.is_bye:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n" + NextGame.teams + '.\nRemember to get your votes in and keep it joyfully agressive!'
else:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n" + NextGame.teams + "\n" + NextGame.time_str + " at " + NextGame.location  + '.\nRemember to get your votes in and keep it joyfully agressive!'


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
    from_=env["TWILIO_PHONE_NUMBER"],
    to=env["MY_NUMBER"]
  )
else:
  for team_member in team_members:
    message = client.messages.create(
      body=message_body,
      from_=env["TWILIO_PHONE_NUMBER"],
      to=team_member
    )