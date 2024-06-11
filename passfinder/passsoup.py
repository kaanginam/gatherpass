from bs4 import BeautifulSoup
import requests
class PassSoup:
    def __init__(self, url) -> None:
        self.url = url
        print(url)
        res = requests.get(url)
        self.soup = BeautifulSoup(res.text, features="html.parser")
    def get_hrefs(self):
        return self.soup.find_all('a', href=True)
    