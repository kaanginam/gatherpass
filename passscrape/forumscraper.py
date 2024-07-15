# from seleniumbase import BaseCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
from passscrape.passnotifier import notify
import time
import logging
import sys
class ForumScraper():
    def __init__(self, urls, parser, config, prefix='', basedir=''):
        self.urls_to_gather = urls
        self.db = PassDB(prefix)
        self.parser = parser
        self.config = config
        self.basedir = basedir
    def scrape(self, forum, blob):
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
        if self.config.get_user_data_dir():
            options.add_argument(
                f"--user-data-dir={self.config.get_user_data_dir()}"
                )
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            #options.add_argument('--incognito')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--remote-debugging-pipe')
        driver = webdriver.Chrome(options=options)
        logging.info("Retrieving posts")
        driver.get(full_url)
        #table_id = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, forum['tid'])))
        table_id = self.wait_for_element(driver, By.ID, forum['tid'])
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        tpc = self.config.get_ntfy_topic()
        for i in range(len(rows)):
            try:
                breakpoint()
                el = rows[i].find_element(By.TAG_NAME, 'a')
                thread = el.get_attribute('href')
                if self.db.thread_exists(forum['name'], thread):
                    continue
                else:
                    self.db.add_thread(forum['name'], thread)
                driver.get(thread)
                leak_content = self.wait_for_element(driver, By.XPATH, forum['post_content']).text
                op = self.get_op(driver, forum)
                self.grab_links(op, forum['name'], tpc)
                if forum['unlike'] not in op.text:
                    
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
                    driver.get(thread)
                    op = self.get_op(driver, forum)
                    leak_content = op.find_element(By.XPATH, forum['post_content']).text
                logging.info("Checking for actual leaks")
                output = self.parser.has_credentials(leak_content)
                if output:
                    filename = f"T_{forum['name']}_{op.get_property('id')}"
                    notify(tpc, f'Thread {thread} is probably a leak: {leak_content} with password {output}')
                else:
                    filename = f"F_{forum['name']}_{op.get_property('id')}"
                    notify(tpc, f'Got thread {thread} post with text: {leak_content}')
                if self.config.get_use_azure():
                    blob.upload(self.basedir, filename, op.text)
                else:
                    with open(f"T_{forum['name']}_{op.  get_property('id')}", "w") as f:
                        f.write(op.text)
                logging.info("Waiting a bit to simulate humanity")
                time.sleep(10)
                # Reopen page, then reload rows array. Not doing this results in an error
                driver.get(full_url)
                table_id = self.wait_for_element(driver, By.ID, forum['tid'])
                rows = table_id.find_elements(By.TAG_NAME, "tr")
            except (NoSuchElementException, StaleElementReferenceException) as e:
                logging.exception(f"{e}")
                continue
    def response(self):
        return "thanks! :D"
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