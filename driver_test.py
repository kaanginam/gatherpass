
#https://forums.raspberrypi.com/viewtopic.php?p=2155925#p2155925
# use sudo apt install chromium-chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service = Service('/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-pipe')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://forums.raspberrypi.com')
print(driver.title)
driver.quit()
