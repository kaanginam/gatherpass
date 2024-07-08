import re
import os
import hashlib
import requests
import time
import enchant
from bs4 import BeautifulSoup
class LeakParser:
    def __init__(self, passlist, providers, config):
        self.passlist = self.get_lines(passlist)
        self.providers = providers
        self.config = config
    def check_patterns(self, string):
        retcode = 0
        for sep in self.config.get_seperators():
            p = re.compile(f"[^{sep}]*" + sep + f"{1}[^sep]*")
            if p.match(string):
                return retcode, sep
            retcode += 1
        return -1
    def has_credentials(self, text):
        retcode = 0
        for pw in self.passlist:
            if pw in text:
                retcode = 1
        for prov in self.providers:
            if prov in text:
                retcode =  2
        return retcode
    def password_in_hibp(pw):
        hexxed = hashlib.sha1(pw.encode()).hexdigest()
        try:
            res = requests.get(f"https://api.pwnedpasswords.com/range/{hexxed[0:5]}")
        except requests.exceptions.ConnectionError:
            time.sleep(30)
            res = requests.get(f"https://api.pwnedpasswords.com/range/{hexxed[0:5]}")
        if res.status_code != 200:
            print("Too many requests!!")
            return False
        hashlist = res.text.split('\n')
    
        for h in hashlist:
            if hexxed.upper() == (hexxed[0:5].upper()+h.strip().split(":") [0]):
                return True
        return False
    def guess_n(self, text):
        return round(len(text.split('\n'))*self.config.get_ratio())
    def has_credentials_n(self, text, passlist, seperators):
        #cnt = 0
        #n = self.guess_n(text)
        with open(passlist, 'r') as f:
            passwords = f.readlines()
        """
        for pw in self.passlist:
            if pw in text:
                cnt += 1
        """
        # TODO: Check for combos
        # Common table formats etc
        # Otherwise: divide words
        lines = text.split("\n")
        
        pw_count = 0
        # TODO: add password regex?
        for line in lines:
            words = []
            words.append(line)
            if " " in line:
                for s in line.split(" "):
                    words.append(s)
            for word in words:
                for sep in seperators:
                    if sep in word: 
                        for s in word.split(sep):     
                            words.append(s)
            for word in words:
                #if d.check(word):
                #    continue
                hexxed = hashlib.sha1(word.encode()).hexdigest()
                if hexxed in passwords:
                    return True
        return False
    def get_lines(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()
    def get_full_text(self, filename):
        with open(filename, 'r') as f:
            return f.read()