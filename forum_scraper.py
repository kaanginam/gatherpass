from datetime import date
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.forumscraper import ForumScraper
import os
from passscrape.passdb import PassDB
today = date.today()
config = PassConfig('./conf.json')
db = PassDB()
from seleniumbase import BaseCase
case = BaseCase()
# https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/
def scrape(forum):
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    scr = ForumScraper(forum, config.get_urls_to_gather(), parser)
    scr.scrape()
def main():
    # parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    for forum in config.get_forums():
        if 'nulled' in forum['name']:
            continue
        scrape(forum)
    
if __name__ == "__main__":
    main()