from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
import requests
import os
class GoogleScraper():
    def __init__(self, cookies, today, config, basedir):
        self.cookies = cookies
        self.today = today
        self.config = config
        self.db = PassDB()
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
                pasteid = pasteurl.split('/')[-1] if pasteurl[-1] != '/' else pasteurl[:-1].split('/')[-1]
                if r'%3F' in pasteid:
                    pasteid = pasteid.split(r'%3F')[0]
                filename = f"{p['site']}_{pasteid}.txt"
                results.append(filename)
                full_url = f"https://{p['site']}/{str(pasteid)}{p['dl']}" if 'reverse' in p and p['reverse'] else f"https://{p['site']}/{p['dl']}{str(pasteid)}"
                res = requests.get(full_url)
                text = res.text
                if self.db.paste_exists(p['site'], pasteid):
                    continue
                # NOTE: SAVING FILE FOR CHECKING RESULTS
                self.db.add_paste(p['site'], pasteid, text)
                with open(self.basedir + filename, 'w') as f:
                    f.write(text)
                # True positive assumed
                output = parser.has_credentials(text, self.config.get_passlist(), self.config.get_seperators())
                if output:
                    print(f"A commonly used password was found on {p['site']}: {pasteurl}. Adding to list")
                    self.db.paste_is_leak(p['site'], pasteid, output)
                    os.rename(self.basedir + filename, self.basedir + f'T_{filename}')
                # False password
                else:
                    print(f"Unsuccesful finding a password, renaming to F_{filename}")
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