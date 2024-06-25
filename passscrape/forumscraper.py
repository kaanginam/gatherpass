# from seleniumbase import BaseCase
from selenium import webdriver
from seleniumbase import SB
from selenium.webdriver.common.by import By
import seleniumbase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from passscrape.passdb import PassDB
from passscrape.passsoup import PassSoup
from bs4 import BeautifulSoup
from passscrape.leakparser import LeakParser
class ForumScraper():
    def __init__(self, forum, urls, parser):
        self.fname = forum['name']
        self.dumplist = forum['dump_list']
        # self.driver = seleniumbase.Driver(uc=True)
        self.tid = forum['tid']
        self.luri = forum['login_uri']
        self.username = forum['username']
        self.password = forum['password']
        self.urls_to_gather = urls
        self.db = PassDB()
        self.parser = parser
    def login(self, base):
        # click on login
        #self = seleniumbase.Driver(uc=True)
        
        breakpoint()
        with SB(uc=True, test=True, chromium_arg="--user-data-dir=~/Library/Application Support/Google/Chrome/Default") as sb:
            sb.driver.uc_open_with_reconnect(f"{base}{self.luri}", reconnect_time=2)
            # breakpoint()
            
            try:
                if sb.driver.find_element(By.TAG_NAME, "iframe"):
                    self.click_turnstile_and_verify(sb)
            except Exception:
                sb.driver.uc_open_with_reconnect(f"{base}{self.luri}", reconnect_time=2)
                self.click_turnstile_and_verify(sb)
            sb.driver.find_element(By.ID, "username").send_keys(self.username)
            sb.driver.find_element(By.ID, "password").send_keys(self.password)
            sb.driver.save_screenshot('Entered_data.png')
            #sb.driver.uc_click()
            sb.driver.find_element(By.XPATH, "//input[@type='button' and value='login']").uc_click()
        
    def scrape(self):
        source = self.fname
        base_url = f"https://{source}"
        full_url = f"{base_url}{self.dumplist}"
        result = ''
        options = webdriver.ChromeOptions()
        # TODO: need to document what os needs what path, and need to write that it takes about
        # 1-2 manual interactions to make it work
        options.add_argument("--user-data-dir=~/Library/Application Support/Google/Chrome/Default")
        driver = webdriver.Chrome(options=options)
        # driver.get(base_url)
        # self.open(full_url)
        # self.click('div[id="tid-link-1623774"]')
        driver.get(full_url)
        table_id = driver.find_element(By.ID, self.tid)
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        #print(self.tid)
        #breakpoint()
        #elements = self.driver.find_element(By.ID, f'{self.tid}')
        #breakpoint()
        for row in rows:
            # breakpoint()
            try:
                el = row.find_element(By.TAG_NAME, 'a')
                thread = el.get_attribute('href')
                if self.db.thread_exists(self.fname, thread):
                    continue
                else:
                    self.db.add_thread(self.fname, thread)
                thread_driver = seleniumbase.Driver(uc=True)
                thread_driver.get(thread)
                posts = thread_driver.find_element(By.ID, 'posts')
                divs = posts.find_elements(By.XPATH, '//div[@class="post_body scaleimages"]')
                op = divs[0]
                #header = thread_driver.find_element(By.CLASS_NAME, 'thread-header')
                # filename = f"{self.fname}_{op.get_property('id')}.txt"
                self.grab_links(op, thread)
                if self.parser.has_credentials_n(op.text):
                    with open(f"T_{self.fname}_{op.get_property('id')}", "w") as f:
                        f.write(op.text) 
                #with open(filename, 'w') as f:
                #    f.write(op.text)
                # TODO: parse leaks
                # TODO: grab telegram links
                # self.check_for_samples(op)
                # if 
                thread_driver.quit()
                # breakpoint()
            except NoSuchElementException as e:
                continue
    def grab_links(self, op, thread):
        soup = BeautifulSoup(op.get_attribute("innerHTML"), features="html.parser")
        hrefs = soup.find_all('a', href=True)
        # srcs = soup.find_all('img')
        for url in self.urls_to_gather:
            for href in hrefs:
                if url in href['href']:
                    self.db.add_links(self.fname, href['href'])
    # def reply(self, c):
    #    c.click()
    
    #def ()
    # from seleniumbase docs
    def click_turnstile_and_verify(self, sb):
        sb.switch_to_frame("iframe")
        sb.driver.uc_click("span")
        sb.assert_element("div#recaptcha-checkbox-checkmark", timeout=3)
    def check_for_samples(self, op):
        breakpoint()
        #if 'sample' in op.text:
        #    print('sample')
        