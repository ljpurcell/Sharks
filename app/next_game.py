from scraper import Season

still_to_play = []

for rnd in Season:
    if not rnd.been_played:
        still_to_play.append(rnd)

NextGame = still_to_play[0] 

for rnd in still_to_play:
    if rnd.date_time < NextGame.date_time:
        NextGame = rnd

