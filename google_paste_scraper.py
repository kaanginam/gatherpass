from datetime import date, timedelta
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
import sys
"""
Main command to run scraper
"""
today = date.today() - timedelta(days=1)
def main():
    # Load config
    config = PassConfig('./conf.json')
    # Initialize parser
    parser = LeakParser(
        config.get_passlist(), 
        config.get_seperators(),
        config.get_ignore_list(),
        config.get_ratio(),
        config.get_any_pw()
        )
    # Initialize scraper
    scraper = GoogleScraper(
        parser,
        config.get_cookies(),
        today,
        config.get_urls_to_gather(),
        config.get_ntfy_topic(),
        config.get_debug(), 
        'pastes/'
    )
    
    # Scan each paste page seperately for pastes
    for p in config.get_paste_pages():
        scraper.scrape(parser, p)
if __name__ == "__main__":
    main()