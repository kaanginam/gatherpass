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
    def __init__(self, parser, cookies, today,  urls_to_gather, tpc, debug,basedir=''):
        self.parser = parser
        self.cookies = cookies
        self.today = today
        self.db = PassDB("scraped_pastes.db", basedir)
        self.basedir = basedir
        self.debug = debug
        self.urls_to_gather = urls_to_gather
        self.tpc = tpc
    def scrape(self, parser, p):
        if self.debug:
            root = logging.getLogger()
            root.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)
        tpc = self.tpc
        req_text = f"site:{p['site']} after:{self.today}"
        page = f'google.com/search?q={req_text}'.replace(" ", "+").replace(":", "%3A").replace("@", "%40")
        logging.info(f'Scanning using query {page}')
        res = requests.get(f'https://{page}', cookies = self.cookies )
        soup = BeautifulSoup(res.text, features='html.parser')
        href_list = soup.find_all('a', href=True)
        # Check all hrefs for paste pages
        for a in href_list:
            url = a['href']
            if f"https://{p['site']}" in url:
                # Get url of the page, filter out any google parameters
                pasteurl = a['href'].split('&')[0].split('=')[1]
                # Paste pages use an id, get that
                pasteid = pasteurl.split('/')[-1] if pasteurl[-1] != '/' else pasteurl[:-1].split('/')[-1]
                # Some pasteids scanned included this specific character. It is not compatible with the rest of
                # the code and is hence removed.
                if r'%3F' in pasteid:
                    pasteid = pasteid.split(r'%3F')[0]
                if self.db.paste_exists(p['site'], pasteid):
                    continue
                filename = f"{p['site']}_{pasteid}.txt"
                # Some paste pages put the URL extension defining the "raw" text behind the id of the paste
                full_url = f"https://{p['site']}/{str(pasteid)}{p['dl']}" if 'reverse' in p and p['reverse'] else f"https://{p['site']}/{p['dl']}{str(pasteid)}"
                res = requests.get(full_url)
                text = res.text
                logging.info(f'Found a new paste')
                self.db.add_paste(p['site'], pasteid, text)
                output, words = self.parser.has_credentials(text)
                addition = ''
                if output:
                    msg = f"A commonly used password was found on {p['site']}: {pasteurl}. The password was {[w for w in words if w['is_pw']]}"
                    logging.info(msg)
                    if tpc:
                        notify(tpc, msg)
                    self.db.paste_is_leak(p['site'], pasteid, output)
                    addition = 'T_'
                    # Only grab links from leaks as they can be interesting and possibly related to the leak
                    self.grab_links(text, p)
                else:
                    addition = 'F_'
                filename = self.basedir + addition + filename
                logging.info(f"Saving text of paste to {filename}")
                self.db.save_results(filename, text, p['site'])
    # Gets all links from a text based on which links
    # are supposed to be gathered
    def grab_links(self, text, p):
        for url in self.urls_to_gather:
            logging.info(f'Trying to get {url} from paste')
            if url in text:
                to_split = url
                if to_split[-1] == '/':
                    to_split = to_split[:-1]
                splitted = text.split(to_split)
                i = 1
                for i in range(1, len(splitted)):
                    to_add = splitted[i]
                    if " " in to_add:
                        spl = to_add.split(" ")
                        to_add = spl[0]
                    if "\n" in to_add:
                        spl = to_add.split('\n')
                        to_add = spl[0]
                    logging.info(f'Adding URL {to_split+to_add}')
                    notify(text, f'Adding URL {to_split+to_add}')
                    self.db.add_links(p, to_split+to_add)