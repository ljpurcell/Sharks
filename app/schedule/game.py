from datetime import datetime

class Game:
    def __init__(self, season_id: int, round: str, date_time: datetime, location: str, teams: str):
        import datetime
        self.season_id = season_id
        self.round = round
        self.date_time = date_time
        self.time_str = self.date_time.strftime("%I:%M %p") 
        self.date_str = self.date_time.strftime("%A %d/%b/%y")
        self.location = location
        self.teams = teams
        self.been_played = self.date_time < datetime.datetime.now()
        self.is_bye = self.location == "BYE"