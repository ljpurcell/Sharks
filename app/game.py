class Game:
    def __init__(self, round, date_time, location, teams):
        import datetime
        self.round = round
        self.date_time = date_time # datetime.datetime.strptime("%I:%M %p, %a, %d %b %y", date_time)
        self.location = location
        self.teams = teams
        #self.been_played = self.date_time < datetime.datetime.now()