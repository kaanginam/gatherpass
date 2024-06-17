# from seleniumbase import BaseCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import seleniumbase
from selenium.common.exceptions import NoSuchElementException
class ForumScraper():
    def __init__(self, forum):
        self.fname = forum['name']
        self.dumplist = forum['dump_list']
        self.driver = seleniumbase.Driver(uc=True)
        self.tid = forum['tid']
    def scrape(self):
        source = self.fname
        base_url = f"https://{source}"
        full_url = f"{base_url}{self.dumplist}"
        # self.open(full_url)
        # self.click('div[id="tid-link-1623774"]')
        self.driver.get(full_url)
        table_id = self.driver.find_element(By.ID, self.tid)
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
                thread_driver = seleniumbase.Driver(uc=True)
                thread_driver.get(thread)
                posts = thread_driver.find_element(By.ID, 'posts')
                divs = posts.find_elements(By.TAG_NAME, 'div')
                op = divs[0]
                self.check_for_samples(op)
                thread_driver.quit()
                # breakpoint()
            except NoSuchElementException as e:
                continue
            
    # def reply(self, c):
    #    c.click()
    #def ()
    def check_for_samples(op):
        if 'sample' in op.text:
            print('sample')
        