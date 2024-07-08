# from seleniumbase import BaseCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
class ForumScraper():
    def __init__(self, forum, urls, parser):
        self.fname = forum['name']
        self.dumplist = forum['dump_list']
        self.tid = forum['tid']
        self.luri = forum['login_uri']
        self.username = forum['username']
        self.password = forum['password']
        self.urls_to_gather = urls
        self.db = PassDB()
        self.parser = parser
        
    def scrape(self):
        source = self.fname
        base_url = f"https://{source}"
        full_url = f"{base_url}{self.dumplist}"
        result = ''
        options = webdriver.ChromeOptions()
        # TODO: need to document what os needs what path, and need to write that it takes about
        # 1-2 manual interactions to make it work
        #options.add_argument("--user-data-dir=~/Library/Application Support/Google/Chrome/Default")
       # options.add_argument(r"--user-data-dir=~/mnt/c/Users/Kaneki\ Ken/AppData/Local/Google/Chrome/User\ Data")
        #options.add_argument("--user-data-dir=~/.config/chromium/Default")
        # options.add_argument("--user-data-dir=~/data_dir/")
        #options.add_argument("--user-data-dir=C:\\Users\Kaneki Ken\\AppData\\Local\\Google\\Chrome\\User Data")
        driver = webdriver.Chrome(options=options)
        driver.get(full_url)
        breakpoint()
        table_id = driver.find_element(By.ID, self.tid)
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                el = row.find_element(By.TAG_NAME, 'a')
                thread = el.get_attribute('href')
                if self.db.thread_exists(self.fname, thread):
                    continue
                else:
                    self.db.add_thread(self.fname, thread)
                driver.get(thread)
                driver.find_element(By.CLASS_NAME, 'postbit_thanks add_tyl_button').click()
                driver.find_element(By.CLASS_NAME, 'postbit_quote').click()
                posts = driver.find_element(By.ID, 'posts')
                divs = posts.find_elements(By.XPATH, '//div[@class="post_body scaleimages"]')
                op = divs[0]
                self.grab_links(op)
                breakpoint()
                output = self.parser.has_credentials(op.text)
                if output:
                    with open(f"T_{self.fname}_{op.get_property('id')}", "w") as f:
                        f.write(op.text) 
                # TODO: parse leaks
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(e)
                print(breakpoint())
                continue
    def grab_links(self, op):
        soup = BeautifulSoup(op.get_attribute("innerHTML"), features="html.parser")
        hrefs = soup.find_all('a', href=True)
        for url in self.urls_to_gather:
            for href in hrefs:
                if url in href['href']:
                    self.db.add_links(self.fname, href['href'])
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