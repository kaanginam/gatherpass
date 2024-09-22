from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
from passscrape.passnotifier import notify
import time
import logging
import sys
import random
import os
from fake_useragent import UserAgent
"""
Deals with scanning forums using customised settings
"""
class ForumScraper():
    def __init__(self, urls, parser, user_data_dir, chrome_binary, tpc, debug, prefix='', basedir=''):
        self.urls_to_gather = urls
        self.db = PassDB("scraped_threads.db", prefix)
        self.parser = parser
        self.tpc = tpc
        self.debug = debug
        self.user_data_dir = user_data_dir
        self.chrome_binary = chrome_binary
        self.basedir = basedir
    """
    Using a given forum object, scrape it
    """    
    def scrape(self, forum, login=False):
        # Obtaining a random user agent
        ua = UserAgent()
        user_agent = ua.random
        if self.debug:
            root = logging.getLogger()
            root.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)
        source = forum['name']
        base_url = f"https://{source}"
        full_url = f"{base_url}{forum['dump_list']}"
        options = webdriver.ChromeOptions()
        # This line is important for some OSes, as the default paths for the chromedriver do not always
        # work with selenium
        if self.chrome_binary:
            service = Service(executable_path=self.chrome_binary)
        else:
            service = Service()
        if self.user_data_dir:
            options.add_argument(f"--user-data-dir={self.user_data_dir}")
        options.add_argument("disable-extensions")
        if os.path.isdir(self.user_data_dir) and not login:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-pipe')
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Retrieving posts")
        driver.get(full_url)
        if login:
            breakpoint()
            return
        if self.debug:
            driver.save_screenshot(f"{forum['name']}-{time.time()}.png")
        table_id = self.wait_for_element(driver, By.ID, forum['tid'])
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        for i in range(len(rows)):
            try:
                el = rows[i].find_element(By.TAG_NAME, 'a')
                thread = el.get_attribute('href')
                if self.db.thread_exists(forum['name'], thread):
                    continue
                else:
                    self.db.add_thread(forum['name'], thread)
                driver.get(thread)
                driver.save_screenshot("frontpage.png")
                
                hidden_existed = False
                leak_content = self.wait_for_element(driver, By.CLASS_NAME, forum['post_content'])
                try:
                    # If the content is not loaded, does not exist anymore or has no text, catch it then just skip
                    leak_content = leak_content.text
                except AttributeError:
                    continue
                if forum['hidden'] in leak_content:
                    hidden_existed = True
                op = self.get_op(driver, forum)
                self.grab_links(op, forum['name'], self.tpc)
                if forum['unlike'] not in op.text and forum['hidden'] in op.text:
                    logging.info("Posts was not liked")
                    bottom_row = op.find_element(By.XPATH, forum['post_bottom'])
                    logging.info("Liking")
                    bottom_row.find_element(By.XPATH, forum['thanks']).click()
                    bottom_row.find_element(By.CLASS_NAME, forum['quote']).click()
                    frame = self.wait_for_element(driver, By.XPATH, forum['reply_body_iframe'])
                    driver.switch_to.frame(frame)
                    reply_body = self.wait_for_element(driver, By.XPATH, forum['reply_body'])
                    reply_body.send_keys(self.response())
                    driver.switch_to.default_content()
                    logging.info("Posting reply")
                    reply_button = self.wait_for_element(driver, By.XPATH, forum['reply_post'])
                    reply_button.click()
                    logging.info("Back to thread")
                    driver.get(thread)
                    logging.info("Getting back the post after reply")
                    op = self.get_op(driver, forum)
                    leak_content = op.find_element(By.CLASS_NAME, forum['post_content'])
                    leak_content = leak_content.text
                logging.info("Checking for actual leaks")
                output = self.parser.has_credentials(leak_content)
                print('reached this part')
                if output or (hidden_existed and forum['hidden'] not in leak_content):
                    filename = f"{self.basedir}T_{forum['name']}_{op.get_property('id')}"
                    if self.tpc:
                        notify(self.tpc, f'Thread {thread} is probably a leak: {leak_content} with content: {leak_content}')
                else:
                    filename = f"{self.basedir}F_{forum['name']}_{op.get_property('id')}"
                    if self.tpc:
                        notify(self.tpc, f'Got thread {thread} post with text: {leak_content}')
                self.db.save_results(filename, leak_content, forum['name'])
                logging.info("Waiting a bit to simulate humanity")
                time.sleep(10)
                # Reopen page, then reload rows array. Not doing this results in an error
                driver.get(full_url)
                table_id = self.wait_for_element(driver, By.ID, forum['tid'])
                rows = table_id.find_elements(By.TAG_NAME, "tr")
            except (NoSuchElementException, StaleElementReferenceException) as e:
                logging.exception(f"{e}")
                continue
    """
    Take a random message created by ChatGPT and then slightly adjusted by me
    """
    def response(self):
        thank_you_messages = [
            "thx",
            "ty :)",
            "cool drop ^^",
            "much appreciated",
            "good stuff",
            "thanks! :D",
            "nice"
        ]
        return random.choice(thank_you_messages)
    """
    Wait for selenium element to exist
    """
    def wait_for_element(self, driver, by, path):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, path)))
            return element 
        except TimeoutException as e:
            logging.exception(f"{e}")
            return None
    """
    Get text of the first post of thread, by the original poster
    """
    def get_op(self, driver, forum):
        posts = self.wait_for_element(driver, By.ID, forum['posts'])
        divs = posts.find_elements(By.XPATH, f'//div[@class="{forum["post_body"]}"]')
        op = divs[0]
        return op
    """
    Grab links from original posts by getting the HTML, then looking for all hrefs
    """
    def grab_links(self, op, fname, tpc):
        soup = BeautifulSoup(op.get_attribute("innerHTML"), features="html.parser")
        hrefs = soup.find_all('a', href=True)
        for url in self.urls_to_gather:
            for href in hrefs:
                if url in href['href']:
                    logging.info(f'Adding link {url} to database')
                    self.db.add_links(fname, href['href'])
                    notify(tpc, f"Got link {href['href']} from {fname}")