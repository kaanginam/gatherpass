import requests
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
import cloudscraper
# https://www.coursehero.com/file/102140146/LISTtxt/
from selenium import webdriver
from passfinder.leakparser import LeakParser
from passfinder.passconfig import PassConfig
from passfinder.passsoup import PassSoup
from passfinder.forumscraper import ForumScraper
import os
from passfinder.passdb import PassDB
#browser = webdriver.Chrome()
today = date.today()
config = PassConfig('./conf.json')
db = PassDB()
scraper = cloudscraper.create_scraper()
from seleniumbase import BaseCase
case = BaseCase()
# https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/
def page_list(forum):
    scr = ForumScraper(forum)
    scr.scrape()
    #driver.quit()
    breakpoint()
def new_posts(forum):
    res = page_list(forum)
    #source = forum['name']
    #base_url = f"https://{source}"
    # soup = PassSoup(f"{base_url}{forum['dump_list']}")
    #breakpoint() 
    #hrefs = soup.get_hrefs()
    #if len(hrefs) == 0:
    #    print("Someethjing wrong")
    #    return
    """
    for a in hrefs:
        link = a['href']
        if f"{base_url}{forum['topics']}" in link:
            splitted = link.split("/")
            splitted = [x for x in splitted if x]
            header = splitted[-1]
            if not db.check_topics(header=header, source=source):
                db.add_topic(header=header, source=source)
                breakpoint()
            # breakpoint()
        else:
            print(a)
    """
def main():
    
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    for forum in config.get_forums():
        if 'nulled' in forum['name']:
            continue
        new = new_posts(forum=forum)
    
if __name__ == "__main__":
    main()