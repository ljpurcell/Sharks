def scrape_site(url):
    """
    REF: https://stackoverflow.com/questions/38489386/python-requests-403-forbidden
    """
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return requests.get(url, headers=headers)




URL = "https://www.playhq.com/basketball-victoria/org/sharks-basketball-club-geelong/b78f41ba/gub-community-competitions-summer-202223/teams/bull-sharks-div2-men/4b014ac5"

page = scrape_site(URL)

print(page.text)

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")

fixture = soup.find('div', {"data-testid": "fixture-list"})

print(fixture.prettify())
    