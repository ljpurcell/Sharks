from os import environ as env
from os.path import join
from twilio.rest import Client
from dotenv import load_dotenv
from next_and_prev_game import PrevGame

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = join('/Users/LJPurcell/Code/Sharks/.env')
load_dotenv(dotenv_path=dotenv_path)

client = Client(env["TWILIO_ACCOUNT_SID"], env["TWILIO_AUTH_TOKEN"])

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
            from_=env["TWILIO_PHONE_NUMBER"],
            to=team_member
        )
