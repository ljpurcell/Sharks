URL = "https://www.playhq.com/basketball-victoria/org/sharks-basketball-club-geelong/b78f41ba/gub-community-competitions-summer-202223/teams/bull-sharks-div2-men/4b014ac5"

def scrape_site(url):
    """
    REF: https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
    """
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return requests.get(url, headers=headers)


page = scrape_site(URL)

from bs4 import BeautifulSoup

soup = BeautifulSoup(page.content, "html.parser")
rounds = soup.find_all('div', {"data-testid": "fixture-list"})

def create_season(rounds):
    from game import Game

    def get_date_time(round):
        from datetime import datetime

        dt = round.find("span", {"class":"sc-bqGHjH cUXLAP"})
        if dt != None:
            # Game is not a BYE and has both date and time
            return datetime.strptime(dt.text, "%I:%M %p, %a, %d %b %y")
        else:
            # Game is a BYE and just has a date
            d = round.find("span", {"class":"sc-bqGHjH keiYNe"})
            return datetime.strptime(d.text, "%A, %d %B %Y")

    def get_teams(round):
        tms = round.find_all("a", {"class":"sc-bqGHjH sc-12j2xsj-3 uheqx gnPplJ"})
        return "Bull Sharks - BYE" if len(tms) < 2 else f"{tms[0].text} vs. {tms[1].text}"

    def create_game(round):
        rnd = round.find("h3", {"class":"sc-bqGHjH sc-10c3c88-1 kqnzOo bFFhqL"}).text
        dt = get_date_time(round)
        loc = "BYE" if round.find("a", {"class":"sc-bqGHjH sc-10c3c88-16 kAtjCO ckPhRR"}) == None else round.find("a", {"class":"sc-bqGHjH sc-10c3c88-16 kAtjCO ckPhRR"}).text
        tms = get_teams(round)
        return Game(rnd, dt, loc, tms)

    season = []
    for round in rounds:
        season.append(create_game(round))
        
    
    return season


Season = create_season(rounds)
