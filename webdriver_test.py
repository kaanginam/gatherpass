from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options = Options()
        # TODO: need to document what os needs what path, and need to write that it takes about
options.add_argument(
    f"--user-data-dir=/home/inam/gatherpass/chrome-data"
)
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-pipe')
options.add_argument('--proxy-server=131.220.5.4:3128')
#options.add_experimental_option("debuggerAddress", "localhost:6666")
driver = webdriver.Chrome(service=Service(executable_path='./chrome', port=3000), options=options)
driver.get('https://google.com')