from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.forumscraper import ForumScraper
import sys
import logging
"""
Main function to scrape forums
"""
def main():
    config = PassConfig('./conf.json')
    parser = LeakParser(
        config.get_passlist(), 
        config.get_seperators(),
        config.get_ignore_list(),
        config.get_ratio(),
        config.get_any_pw()
    )
    scr = ForumScraper(
        config.get_urls_to_gather(), 
        parser,
        config.get_user_data_dir(),
        config.get_chrome_binary(),
        config.get_ntfy_topic(), 
        config.get_debug(),
        prefix='', 
        basedir='threads/'
    )
    if config.get_debug():
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
    login = False
    if len(sys.argv) > 1 and sys.argv[1] == 'login':
        login = True
    # For each forum, scrape using created parser
    for forum in config.get_forums():
        logging.info(f"Scanning {forum['name']}'s list {forum['dumplist']}")
        scr.scrape(forum, login)
    
if __name__ == "__main__":
    main()