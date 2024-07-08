import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
import urllib.request
# https://www.coursehero.com/file/102140146/LISTtxt/
from selenium import webdriver
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
import os
from passscrape.passdb import PassDB
from passscrape.googlescraper import GoogleScraper
today = date.today() - timedelta(days=1)
"""Main function to get scraps

Keyword arguments:
Return: if a paste has leak or not
"""

def main():
    # Load the db, is for collecting pastes
    db = PassDB()
    config = PassConfig('./conf.json')
    cookies = config.get_cookies()
    scraper = GoogleScraper(cookies, today, config, db, 'pastes/')
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    for p in config.get_paste_pages():
        scraper.scrape(parser, p)
if __name__ == "__main__":
    main()