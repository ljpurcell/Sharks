from os import environ as env
from os.path import join
from twilio.rest import Client
from dotenv import load_dotenv

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = join('/Users/LJPurcell/Code/Sharks/.env')
load_dotenv(dotenv_path=dotenv_path)

client = Client(env["TWILIO_ACCOUNT_SID"], env["TWILIO_AUTH_TOKEN"])

from next_and_prev_game import NextGame

if NextGame.is_bye:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n" + NextGame.teams
else:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n" + NextGame.teams + "\n" + NextGame.time_str + " at " + NextGame.location


team_members = [
  "+61447915198", # Me
  "+61447615707", # Walt
  "+61488920388", # AJ    
  "+61427987353", # IJ
  "+61429867267", # Reece
  "+61407506565", # Vin
  "+61447744628", # Nick
]

for team_member in team_members:
  message = client.messages.create(
    body=message_body,
    from_="+15154617756",
    to=team_member
  )