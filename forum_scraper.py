import requests
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
# https://www.coursehero.com/file/102140146/LISTtxt/
from selenium import webdriver
from passfinder.leakparser import LeakParser
from passfinder.passconfig import PassConfig
from passfinder.passsoup import PassSoup
import os
from passfinder.passdb import PassDB
browser = webdriver.Chrome()
today = date.today()
config = PassConfig('./conf.json')
db = PassDB()
# https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/
def new_posts(forum):
    source = forum['name']
    base_url = f"https://{source}"
    soup = PassSoup(f"{base_url}{forum['dump_list']}")
    hrefs = soup.get_hrefs()
    if len(hrefs) == 0:
        print("So,ethjing wrong")
        return
    for a in hrefs:
        link = a['href']
        if f"{base_url}{forum['topics']}" in link:
            splitted = link.split("/")
            splitted = [x for x in splitted if x]
            header = splitted[-1]
            if not db.check_topics(header=header, source=source):
                db.add_topic(header=header, source=source)
            # breakpoint()
        else:
            print(a)
def main():
    
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    for forum in config.get_forums():
        new = new_posts(forum=forum)
    
if __name__ == "__main__":
    main()