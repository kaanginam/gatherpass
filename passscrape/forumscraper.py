# from seleniumbase import BaseCase
from selenium import webdriver
import undetected_chromedriver as uc
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
from seleniumbase import Driver
"""
Deals with scanning forums using customised settings
"""
class ForumScraper():
    def __init__(self, urls, parser, config, prefix='', basedir=''):
        self.urls_to_gather = urls
        self.db = PassDB("scraped_threads.db", prefix)
        self.parser = parser
        self.config = config
        self.basedir = basedir
    def scrape(self, forum):
        ua = UserAgent()
        user_agent = ua.random
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
        # TODO: need to document what os needs what path, and need to write that it takes about
        if self.config.get_chrome_binary():
            print("hello0")
            service = Service(executable_path=self.config.get_chrome_binary())
        else:
            service = Service()
        if self.config.get_user_data_dir():
            options.add_argument(
                f"--user-data-dir={self.config.get_user_data_dir()}"
                )
            options.add_argument("disable-extensions")
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            #options.add_argument('--incognito')
            print(user_agent)
            options.add_argument(f'--user-agent={user_agent}')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-pipe')
            #options.add_argument('--remote-debugging-port=9222')
        driver = webdriver.Chrome(service=service, options=options)
        #driver = Driver(browser="chrome", uc=True, headless=True, user_data_dir=self.config.get_user_data_dir())
        logging.info("Retrieving posts")
        driver.get(full_url)
        
        driver.save_screenshot(f"{time.time()}.png")
        #table_id = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, forum['tid'])))
        table_id = self.wait_for_element(driver, By.ID, forum['tid'])
        driver.save_screenshot(f"{time.time()}.png")
        
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        tpc = self.config.get_ntfy_topic()
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
                    leak_content = leak_content.text
                except AttributeError:
                    continue
                if forum['hidden'] in leak_content:
                    hidden_existed = True
                op = self.get_op(driver, forum)
                self.grab_links(op, forum['name'], tpc)
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
                    notify(tpc, f'Thread {thread} is probably a leak: {leak_content} with content: {leak_content}')
                else:
                    filename = f"{self.basedir}F_{forum['name']}_{op.get_property('id')}"
                    notify(tpc, f'Got thread {thread} post with text: {leak_content}')
                self.parser.save_results(filename, leak_content, forum['name'])
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
    def get_op(self, driver, forum):
        posts = self.wait_for_element(driver, By.ID, forum['posts'])
        divs = posts.find_elements(By.XPATH, f'//div[@class="{forum["post_body"]}"]')
        op = divs[0]
        return op
    def grab_links(self, op, fname, tpc):
        soup = BeautifulSoup(op.get_attribute("innerHTML"), features="html.parser")
        hrefs = soup.find_all('a', href=True)
        for url in self.urls_to_gather:
            for href in hrefs:
                if url in href['href']:
                    self.db.add_links(fname, href['href'])
                    notify(tpc, f"Got link {href['href']} from {fname}")
    def reply_to_thread(self, driver):
        # TODO: find reply button, choose a reply, then reload page after reply
        # driver.
        print('driver')
    def click_turnstile_and_verify(self, sb):
        sb.switch_to_frame("iframe")
        sb.driver.uc_click("span")
        sb.assert_element("div#recaptcha-checkbox-checkmark", timeout=3)
    def check_for_samples(self, op):
        breakpoint()