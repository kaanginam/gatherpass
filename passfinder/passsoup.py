from bs4 import BeautifulSoup
import requests
import cloudscraper
class PassSoup:
    def __init__(self, url) -> None:
        self.url = url
        scraper = cloudscraper.create_scraper()
        # res = requests.get(url)
        self.soup = BeautifulSoup(scraper.get(url).text, features="html.parser")
    def get_hrefs(self):
        return self.soup.find_all('a', href=True)
    