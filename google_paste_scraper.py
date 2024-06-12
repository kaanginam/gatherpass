import requests
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
# https://www.coursehero.com/file/102140146/LISTtxt/
from selenium import webdriver
from passfinder.leakparser import LeakParser
from passfinder.passconfig import PassConfig
import os
from passfinder.passdb import PassDB
#browser = webdriver.Chrome()
today = date.today()

def main():
    db = PassDB()
    config = PassConfig('./conf.json')
    cookies = config.get_cookies()
    paste_parser = LeakParser(config.get_passlist(), config.get_providers(), config)
    for p in config.get_paste_pages():
        req_text = f"site:{p['site']} after:{today}"
        page = f'google.com/search?q={req_text}'.replace(" ", "+").replace(":", "%3A").replace("@", "%40") #+ f'&freshness=day'
        res = requests.get(f'https://{page}', cookies = cookies )
        soup = BeautifulSoup(res.text)#, features=html.parser)
        results = []
        for a in soup.find_all('a', href=True):
            if f"https://{p['site']}" in a['href']:
                pasteurl = a['href'].split('&')[0].split('=')[1]
                
                pasteid = pasteurl.split('/')[-1]
                filename = f"{p['site']}_{pasteid}.txt"
                results.append(filename)
                #print(f"https://{p['site']}/{p['dl']}{str(pasteid)}")
                # breakpoint()
                # urllib.request.urlretrieve(f"https://{p['site']}/{p['dl']}{str(pasteid)}", filename) 
                res = requests.get(f"https://{p['site']}/{p['dl']}{str(pasteid)}")
                
                text = res.text
                # NOTE: SAVING FILE FOR CHECKING RESULTS
                with open(filename, 'w') as f:
                    f.write(text)
                r = paste_parser.has_credentials(text)
                if r == 1:
                    print(f"A commonly used password was found on {p['site']}: {pasteurl}. Adding to list")
                    db.add_accounts_from_file(text=text, source=p['site'], pasteid=pasteid, parser=paste_parser)
                elif r == 2:
                    print(f"A commonly used e-mail service provider was found on {p['site']}: {pasteurl}. Adding to list")
                    db.add_accounts_from_file(text=text, source=p['site'], pasteid=pasteid, parser=paste_parser)
                elif r == 3:
                    print(f"A commonly used table format was found on {p['site']}: {pasteurl}. Adding to list")
                    db.add_accounts_from_file(text=text, source=p['site'], pasteid=pasteid, parser=paste_parser)
                else:
                    print(f"Unsuccesful finding a password, renaming to {filename}_F")
                    os.rename(filename, f'{filename}_F')
if __name__ == "__main__":
    main()