from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.forumscraper import ForumScraper
config = PassConfig('./conf.json')
"""
Main function to scrape forum
"""
def main():
    parser = LeakParser(config.get_passlist(), config)
    scr = ForumScraper(config.get_urls_to_gather(), parser, config, '', 'threads/')
    # For each forum, scrape using created parser
    for forum in config.get_forums():
        if 'nulled' in forum['name']:
            continue
        scr.scrape(forum)
    
if __name__ == "__main__":
    main()