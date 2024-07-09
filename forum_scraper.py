# https://www.coursehero.com/file/102140146/LISTtxt/
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.forumscraper import ForumScraper
config = PassConfig('./conf.json')
# https://www.nulled.to/topic/1620375-81k-leak-website-dump-top-hashed/
def main():
    parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    scr = ForumScraper(config.get_urls_to_gather(), parser, config)
    for forum in config.get_forums():
        if 'nulled' in forum['name']:
            continue
        scr.scrape(forum)
    
if __name__ == "__main__":
    main()