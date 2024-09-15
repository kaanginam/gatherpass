from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.forumscraper import ForumScraper
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
    # For each forum, scrape using created parser
    for forum in config.get_forums():
        scr.scrape(forum)
    
if __name__ == "__main__":
    main()