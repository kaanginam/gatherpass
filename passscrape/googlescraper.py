from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
import requests
from passscrape.passnotifier import notify
import logging
import sys
"""
Deals with scraping using Google Indexing and then deals with scraped content
"""
class GoogleScraper():
    def __init__(self, cookies, today, config, basedir=''):
        self.cookies = cookies
        self.today = today
        self.config = config
        self.db = PassDB("scraped_pastes.db", basedir)
        self.basedir = basedir
    def scrape(self, parser, p):
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        tpc = self.config.get_ntfy_topic()
        req_text = f"site:{p['site']} after:{self.today}"
        page = f'google.com/search?q={req_text}'.replace(" ", "+").replace(":", "%3A").replace("@", "%40")
        logging.info(f'Scanning using query {page}')
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
                # Some paste pages put the URL extension defining the "raw" text behind the id of the paste
                full_url = f"https://{p['site']}/{str(pasteid)}{p['dl']}" if 'reverse' in p and p['reverse'] else f"https://{p['site']}/{p['dl']}{str(pasteid)}"
                res = requests.get(full_url)
                text = res.text
                # Do not check pastes already in database
                if self.db.paste_exists(p['site'], pasteid):
                    continue
                logging.info(f'Found a new paste')
                self.db.add_paste(p['site'], pasteid, text)
                output, words = parser.has_credentials(text)
                addition = ''
                if output:
                    msg = f"A commonly used password was found on {p['site']}: {pasteurl}. The password was {[w for w in self.words if w['is_pw']]}"
                    logging.info(msg)
                    if tpc:
                        notify(tpc, msg)
                    self.db.paste_is_leak(p['site'], pasteid, output)
                    addition = 'T_'
                    # Only grab links from leaks as they can be interesting and possibly related to the leak
                    self.grab_links(tpc, text, p)
                # False password
                else:
                    addition = 'F_'
                filename = self.basedir + addition + filename
                parser.save_results(filename, text, p['site'])
    # Gets all links from a text based on which links
    # are supposed to be gathered
    def grab_links(self, tpc, text, p):
        for url in self.config.get_urls_to_gather():
            logging.info(f'Trying to get {url} from paste')
            if url in text:
                to_split = url
                if to_split[-1] == '/':
                    to_split = to_split[:-1]
                splitted = text.split(to_split)
                to_add = splitted[1]
                if " " in to_add:
                    spl = to_add.split(" ")
                    to_add = spl[0]
                logging.info(f'Adding URL {to_split+to_add}')
                notify(tpc, f'Adding URL {to_split+to_add}')
                self.db.add_links(p, to_split+to_add)