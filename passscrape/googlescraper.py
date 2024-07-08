from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
class GoogleScraper():
    def __init__(self, cookies, today, config, db, basedir):
        self.cookies = cookies
        self.today = today
        self.config = config
        self.db = db
        self.basedir = basedir
    def scrape(self, parser, p):
        req_text = f"site:{p['site']} after:{self.today}"
        page = f'google.com/search?q={req_text}'.replace(" ", "+").replace(":", "%3A").replace("@", "%40") #+ f'&freshness=day'
        res = requests.get(f'https://{page}', cookies = self.cookies )
        soup = BeautifulSoup(res.text, features='html.parser')
        results = []
        href_list = soup.find_all('a', href=True)
        # Check all hrefs for paste pages
        for a in href_list:
            url = a['href']
            if f"https://{p['site']}" in url:
                # Get url of the page, filter out any google parameters
                pasteurl = a['href'].split('&')[0].split('=')[1]
                # Paste pages use an id, get that
                pasteid = pasteurl.split('/')[-1]
                filename = f"{p['site']}_{pasteid}.txt"
                results.append(filename)
                res = requests.get(f"https://{p['site']}/{p['dl']}{str(pasteid)}")
                text = res.text
                if self.db.paste_exists(p['site'], pasteid):
                    continue
                # NOTE: SAVING FILE FOR CHECKING RESULTS
                self.db.add_paste(p['site'], pasteid, text)
                #breakpoint()
                with open(self.basedir + filename, 'w') as f:
                    f.write(text)
                # True positive assumed
                if parser.has_credentials_n(text, self.config.get_passlist(), self.config.get_seperators()):
                    print(f"A commonly used password was found on {p['site']}: {pasteurl}. Adding to list")
                    os.rename(self.basedir + filename, self.basedir + f'T_{filename}')
                # False password
                else:
                    print(f"Unsuccesful finding a password, renaming to {filename}_F")
                    os.rename(self.basedir + filename, self.basedir + f'F_{filename}')
    def grab_links(self, text, p):
        for url in self.config.get_urls_to_gather():
            if url in text:
                to_split = url
                if to_split[-1] == '/':
                    to_split = to_split[:-1]
                splitted = text.split(to_split)
                to_add = splitted[1]
                if " " in to_add:
                    spl = to_add.split(" ")
                    to_add = spl[0]
                self.db.add_links(p, to_split+to_add)