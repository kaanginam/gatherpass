import re
import os
import hashlib
import requests
import time
import enchant
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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
    def is_url(self, line):
        try:
            res = urlparse(line)
            return all([res.scheme, res.netloc])
        except AttributeError:
            return False
    def has_credentials(self, text):
        seperators = self.config.get_seperators()
        #cnt = 0
        #n = self.guess_n(text)
        # TODO: Check for combos
        # Common table formats etc
        # Otherwise: divide words
        lines = text.split("\n")
        pw_count = 0
        # TODO: add password regex?
        for line in lines:
            # there are a lot of lines with just links, skip them here for credential search. 
            if self.is_url(line):
                continue
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
                if hexxed.upper() in self.passlist:
                    return word
        return False
    def get_lines(self, filename):
        with open(filename, 'r') as f:
            return f.read().splitlines()