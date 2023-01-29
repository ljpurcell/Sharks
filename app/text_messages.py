from os import environ as env
from os.path import join
from twilio.rest import Client
from dotenv import load_dotenv

dotenv_path = join('/Users/LJPurcell/Code/Sharks/.env')
load_dotenv(dotenv_path=dotenv_path)

account_sid = "AC43d1269aaba5977f6cff209fba752f99"
auth_token = env["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

from scraper import Season

game = Season[0]

message_body = "First game was:\n" + game.round + ", on " + game.date_time_str + ", at " + game.location + " between " + str(game.teams) + " and it is " + str(game.been_played) + " this game has been played."

message = client.messages.create(
  body=message_body,
  from_="+15154617756",
  to="+61447915198"
)

print(message.sid)