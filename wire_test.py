import seleniumwire.undetected_chromedriver as uc
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(
    options=chrome_options,
    seleniumwire_options={}
)
driver.proxy = { 'https': 'http://131.220.5.4:3128'}
driver.get('https://api.ipify.org?format=json')
driver.proxy = { }
driver.get('https://api.ipify.org?format=json')