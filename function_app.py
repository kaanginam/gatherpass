import logging
import azure.functions as func

app = func.FunctionApp()
from datetime import date, timedelta
from passscrape.forumscraper import ForumScraper
import os
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
from passscrape.azureblobsaver import AzureBlobSaver
import shutil
@app.timer_trigger(schedule="* */30 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def gather_pass(myTimer: func.TimerRequest) -> None:
    today = date.today() - timedelta(days=1)
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Running a scan of paste pages using Google')
    config = PassConfig('./conf.json')
    cookies = config.get_cookies()
    scraper = GoogleScraper(cookies, today, config, '/home/site')
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    blob = AzureBlobSaver(config.get_db_conn_str(), 'output-data')
    for p in config.get_paste_pages():
        logging.info(f'Scraping paste page {p}')
        scraper.scrape(parser, p, blob)
@app.timer_trigger(schedule="* */30 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
def gather_pass_forums(myTimer: func.TimerRequest) -> None:
    today = date.today() - timedelta(days=1)
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Running a scan of forums for leaks, while trying to reply')
    shutil.copy('firefox-data', 'tmp')
    config = PassConfig('./conf.json')
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    blob = AzureBlobSaver(config.get_db_conn_str(), 'output-data')
    scr = ForumScraper(config.get_urls_to_gather(), parser, config,  '', 'threads/')
    for forum in config.get_forums():
        if 'nulled' in forum['name']:
            continue
        scr.scrape(forum, blob)