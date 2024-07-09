# from seleniumbase import BaseCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from passscrape.passdb import PassDB
from bs4 import BeautifulSoup
class ForumScraper():
    def __init__(self, urls, parser, config):
        self.urls_to_gather = urls
        self.db = PassDB()
        self.parser = parser
        self.config = config
    def scrape(self, forum):
        source = forum['name']
        base_url = f"https://{source}"
        full_url = f"{base_url}{forum['dump_list']}"
        options = webdriver.ChromeOptions()
        # TODO: need to document what os needs what path, and need to write that it takes about
        # 1-2 manual interactions to make it work
        #options.add_argument("--user-data-dir=~/Library/Application Support/Google/Chrome/Default")
       # options.add_argument(r"--user-data-dir=~/mnt/c/Users/Kaneki\ Ken/AppData/Local/Google/Chrome/User\ Data")
        #options.add_argument("--user-data-dir=~/.config/chromium/Default")
        # options.add_argument("--user-data-dir=~/data_dir/")
        #options.add_argument("--user-data-dir=C:\\Users\Kaneki Ken\\AppData\\Local\\Google\\Chrome\\User Data")
        if self.config.get_user_data_dir():
            options.add_argument(
                f"--user-data-dir={self.config.get_user_data_dir()}"
                )
        if self.config.get_chrome_binary():
            driver = webdriver.Chrome(self.config.get_chrome_binary(), options=options)
        else:
            driver = webdriver.Chrome(options=options)
        driver.get(full_url)
        table_id = driver.find_element(By.ID, forum['tid'])
        rows = table_id.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                el = row.find_element(By.TAG_NAME, 'a')
                thread = el.get_attribute('href')
                if self.db.thread_exists(forum['name'], thread):
                    continue
                else:
                    self.db.add_thread(forum['name'], thread)
                driver.get(thread)
                #driver.find_element(By.CLASS_NAME, self.forum['thanks']).click()
                #driver.find_element(By.CLASS_NAME, self.forum['quote']).click()
                posts = driver.find_element(By.ID, forum['posts'])
                divs = posts.find_elements(By.XPATH, f'//div[@class="{forum["post_body"]}"]')
                op = divs[0]
                self.grab_links(op, forum['name'])
                breakpoint()
                output = self.parser.has_credentials(op.text)
                if output:
                    with open(f"T_{forum['name']}_{op.get_property('id')}", "w") as f:
                        f.write(op.text) 
                # TODO: parse leaks
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(e)
                print(breakpoint())
                continue
    def grab_links(self, op, fname):
        soup = BeautifulSoup(op.get_attribute("innerHTML"), features="html.parser")
        hrefs = soup.find_all('a', href=True)
        for url in self.urls_to_gather:
            for href in hrefs:
                if url in href['href']:
                    self.db.add_links(fname, href['href'])
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