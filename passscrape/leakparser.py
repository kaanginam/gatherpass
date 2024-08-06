import re
import os
import hashlib
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import enchant
import logging
from langdetect import detect
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
    def get_language(self, text):
        res = detect(text)
        result = ''
        for lg in enchant._broker.list_languages():
            if lg == res:
                result = lg
                break
            elif res in lg:
                result = lg
                break
        if result == '':
            result = 'en_US'
        return result
    def has_credentials(self, text):
        lang = self.get_language(text)
        d = enchant.Dict(lang)
        seperators = self.config.get_seperators()
        #cnt = 0
        #n = self.guess_n(text)
        # TODO: Check for combos
        # Common table formats etc
        # Otherwise: divide words
        lines = text.split("\n")
        pw_count = 0
        # TODO: add password regex?
        words = []
        for line in lines:
            # there are a lot of lines with just links, skip them here for credential search. 
            if self.is_url(line):
                continue
            words.append(line)
            if " " in line:
                for s in line.split(" "):
                    words.append(s)
            for word in words:
                for sep in seperators:
                    if sep in word: 
                        for s in word.split(sep):     
                            words.append(s)
        dict_count = 0
        ignore_list = self.config.get_ignore_list()
        pw_count += 1
        for word in words:
            if d.check(word):
                dict_count += 1
            hexxed = hashlib.sha1(word.encode()).hexdigest()
            # TODO: explain this line
            if (hexxed.upper() in self.passlist or hexxed in self.passlist) and word not in ignore_list and len(word) != 1:
                pw_count += 1
        logging.info(f'pw_count: {pw_count}, dict_count: {dict_count}, ratio: {dict_count/pw_count}')
        if dict_count > pw_count and pw_count != 0 and  dict_count/pw_count > self.config.get_ratio():
            return False
        else:
            return True
    def save_results(self, filename, content, source):
        from datetime import datetime
        ct = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'{ct} from {source}\n')
            f.write(content)
    def get_lines(self, filename):
        with open(filename, 'r') as f:
            return f.read().splitlines()