from datetime import date, timedelta
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper

today = date.today() - timedelta(days=1)

def main():
    config = PassConfig('./conf.json')
    cookies = config.get_cookies()
    scraper = GoogleScraper(cookies, today, config, 'pastes/')
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)


    for p in config.get_paste_pages():
        scraper.scrape(parser, p)
if __name__ == "__main__":
    main()