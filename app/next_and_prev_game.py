from scraper import Season

played = []
still_to_play = []

for rnd in Season:
    if rnd.been_played:
        played.append(rnd)
    else:
        still_to_play.append(rnd)

PrevGame = played[len(played)-1]

for rnd in played:
    if rnd.date_time > PrevGame.date_time:
        PrevGame = rnd


if not still_to_play:
    NextGame = None
else:
    NextGame = still_to_play[0] 
    for rnd in still_to_play:
        if rnd.date_time < NextGame.date_time:
            NextGame = rnd

