import logging
import azure.functions as func

app = func.FunctionApp()
from datetime import date, timedelta
# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
today = date.today() - timedelta(days=1)
@app.schedule(schedule="* */30 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def gather_pass(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    config = PassConfig('./conf.json')
    cookies = config.get_cookies()
    scraper = GoogleScraper(cookies, today, config, 'pastes/')
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    for p in config.get_paste_pages():
        scraper.scrape(parser, p)