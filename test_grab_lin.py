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
    # Initialize scraper
    scraper = GoogleScraper(
        config.get_cookies(),
        today,
        ['https://www.reddit.com'],
        config.get_ntfy_topic(),
        config.get_debug(), 
        'pastes/'
    )
    # Initialize parser
    parser = LeakParser(
        config.get_passlist(), 
        config.get_seperators(),
        config.get_ignore_list(),
        config.get_any_pw()
        )
    with open("fpastes/T_pastebin.com_npXnt8DK.txt", "r") as f:
        text = f.read()
    # Scan each paste page seperately for pastes
    scraper.grab_links(text, {
        "source": "https://www.redit.com",
        "url": "https://tmp.com"
        })
if __name__ == "__main__":
    main()