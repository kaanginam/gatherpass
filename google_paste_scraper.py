from datetime import date, timedelta
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
import sys
import logging
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
    if config.get_debug():
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
    # Scan each paste page seperately for pastes
    for p in config.get_paste_pages():
        logging.info(f"Scanning paste page {p['site']}")
        scraper.scrape(parser, p)
if __name__ == "__main__":
    main()