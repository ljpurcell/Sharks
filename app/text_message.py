from os import environ as env
from os.path import join
from twilio.rest import Client
from dotenv import load_dotenv

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = join('/Users/LJPurcell/Code/Sharks/.env')
load_dotenv(dotenv_path=dotenv_path)

client = Client(env["TWILIO_ACCOUNT_SID"], env["TWILIO_AUTH_TOKEN"])

from next_game import NextGame

if NextGame.is_bye:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n" + NextGame.teams
else:
  message_body = NextGame.round + " - " + NextGame.date_str + "\n" + NextGame.teams + "\n" + NextGame.time_str + " at " + NextGame.location

message = client.messages.create(
  body=message_body,
  from_=env["TWILIO_PHONE_NUMBER"],
  to=env["MY_NUMBER"]
)