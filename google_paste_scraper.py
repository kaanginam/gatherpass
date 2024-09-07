from datetime import date, timedelta
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
"""
Main command to run scraper
"""
today = date.today() - timedelta(days=1)
def main():
    # Load config
    config = PassConfig('./conf.json')
    # Get cookies from config
    cookies = config.get_cookies()
    # Initialize scraper
    scraper = GoogleScraper(cookies, today, config, 'pastes/')
    # Initialize parser
    parser = LeakParser(config.get_passlist(), config)
    # Scan each paste page seperately for pastes
    for p in config.get_paste_pages():
        scraper.scrape(parser, p)
if __name__ == "__main__":
    main()