def scrape_site(url):
    """
    REF: https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
    """
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return requests.get(url, headers=headers)




URL = "https://www.playhq.com/basketball-victoria/org/sharks-basketball-club-geelong/b78f41ba/gub-community-competitions-summer-202223/teams/bull-sharks-div2-men/4b014ac5"

page = scrape_site(URL)

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")

rounds = soup.find_all('div', {"data-testid": "fixture-list"})


def create_season(rounds):
    from game import Game

    def create_game(round):
        # TODO: Handle BYE when no time data is given
        rnd = round.find("h3", {"class":"sc-bqGHjH sc-10c3c88-1 kqnzOo bFFhqL"}).text
        dt = round.find("span", {"class":"sc-bqGHjH cUXLAP"}).text
        loc = "BYE" if round.find("a", {"class":"sc-bqGHjH sc-10c3c88-16 kAtjCO ckPhRR"}) == None else round.find("a", {"class":"sc-bqGHjH sc-10c3c88-16 kAtjCO ckPhRR"}).text
        tms = round.find_all("a", {"class":"sc-bqGHjH sc-12j2xsj-3 uheqx gnPplJ"})
        return Game(rnd, dt, loc, tms)

    season = []
    for round in rounds[:]:
        print(round.prettify())
        season.append(create_game(round))
        
    
    return season


season = create_season(rounds)
print(season[0].date_time)