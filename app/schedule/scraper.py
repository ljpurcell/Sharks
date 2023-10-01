from os import environ as env
from .game import Game
from bs4 import BeautifulSoup, Tag, NavigableString, ResultSet, PageElement
from datetime import datetime
from app.notifications.text_messages.notify_developer import notify_developer


def scrape_site(url: str | None):
    if not url:
        raise ValueError("URL for fixture not found")

    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    response = requests.get(url, headers=headers, timeout=5)
    return response


def create_season(rounds: PageElement) -> list[Game]:
    from .game import Game

    def get_date_time(round: Tag) -> datetime:
        from datetime import datetime

        dt: Tag | NavigableString | None = round.find(
            "span", {"class": "sc-cPiKLX dTddCR"})
        if not dt:
            # Game is a BYE and just has a date
            d: Tag | NavigableString | None = round.find(
                "span", {"class": "sc-bqGHjH keiYNe"})
            return datetime.strptime(d.text, "%A, %d %B %Y")
        else:
            # Game is not a BYE and has both date and time
            return datetime.strptime(dt.text, "%I:%M %p, %a, %d %b %y")

    def get_teams(round: Tag) -> str:
        tms: ResultSet[Tag] = round.find_all(
            "a", {"class": "sc-jEACwC sc-12j2xsj-3 iXloFG cdnZHA"})
        return "Bull Sharks - BYE" if len(tms) < 2 else f"{tms[0].text} vs. {tms[1].text}"

    def create_game(round: Tag) -> Game:
        ssn: str = env.get('SEASON_ID')
        # If site changes, will need to update class tags used here
        rnd_tag = round.find("h3", {"class": "sc-jEACwC sc-10c3c88-1 fLTgUy fLyUTG"}) if round.find("h3", {
            "class": "sc-jEACwC sc-10c3c88-1 fLTgUy fLyUTG"}) else round.find("h3", {"class": "sc-jEACwC sc-10c3c88-1 fLTgUy fLyUTG"})
        if rnd_tag:
            rnd = rnd_tag.text

            if rnd == "Fixture has not yet been confirmed, dates and rounds are subject to change.":
                dt: datetime | None = None
                loc: str | None = None
                tms: str | None = None
            else:
                dt: datetime | None = get_date_time(round)

                # If site changes, will need to update class tags used here
                loc: str | None = "BYE" if round.find("a", {"class": "sc-jEACwC sc-10c3c88-16 dDYSmJ gIKUwU"}
                                                      ) == None else round.find("a", {"class": "sc-jEACwC sc-10c3c88-16 dDYSmJ gIKUwU"}).text
                tms: str | None = get_teams(round)

            return Game(ssn, rnd, dt, loc, tms)
        else:
            # notify_developer()


    season: list[Game] = []
    for round in rounds:
        season.append(create_game(round))

    return season


URL: str | None = env.get('SCHEDULE_URL')

page = scrape_site(URL)

soup: BeautifulSoup = BeautifulSoup(page.content, "html.parser")
rounds = soup.find_all('div', {"data-testid": "fixture-list"})

Season = create_season(rounds)
