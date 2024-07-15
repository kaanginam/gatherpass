from datetime import date, timedelta
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
from passscrape.azureblobsaver import AzureBlobSaver
import os
today = date.today() - timedelta(days=1)

def main():
    config = PassConfig('./conf.json')
    config.set_use_azure(False)
    cookies = config.get_cookies()
    scraper = GoogleScraper(cookies, today, config, '/home/site/')
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    blob = AzureBlobSaver('output-data')
    for p in config.get_paste_pages():
        scraper.scrape(parser, p, blob)
if __name__ == "__main__":
    main()