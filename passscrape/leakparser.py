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
    def word_in_words(self, word, words):
        found = False
        for w in words:
            if w["txt"]== word:
                w["count"] += 1
                found = True
        if not found and word != '' and word != '\n':
            words.append({
                "txt": word, 
                "count": 0,
                "is_pw": False
            })
        return words
    def get_words(self, text):
        seperators = self.config.get_seperators()
        lines = text.split("\n")
        words = []
        for line in lines:
            if self.is_url(line):
                continue
            if line == '\n' or line == '':
                continue
            words = self.word_in_words(line, words)
            wordsInLine = []
            if " " in line:
                for s in line.split(" "):
                    if s != '' and s != '\n':
                        wordsInLine.append(s)
            for word in wordsInLine:
                for sep in seperators:
                    if sep in word: 
                        for s in word.split(sep):   
                            if s != '' and s != '\n':
                                words = self.word_in_words(s, words)           
                words = self.word_in_words(word, words)
        return words
    def has_credentials(self, text):
        lang = self.get_language(text)
        d = enchant.Dict(lang)
        #cnt = 0
        #n = self.guess_n(text)
        # TODO: Check for combos
        # Common table formats etc
        # Otherwise: divide words
        pw_count = 0
        # TODO: add password regex?
        words = self.get_words(text)
        dict_count = 0
        ignore_list = self.config.get_ignore_list()
        pw_count += 1
        for word in words:
            if d.check(word["txt"]) and not word["txt"].isdigit():
                dict_count += 1
            hexxed = hashlib.sha1(word["txt"].encode()).hexdigest()
            # TODO: explain this line
            if (hexxed.upper() in self.passlist or hexxed in self.passlist) and word["txt"] not in ignore_list and len(word["txt"]) != 1:
                pw_count += 1
                word["is_pw"] = True
        logging.info(f'pw_count: {pw_count}, dict_count: {dict_count}, ratio: {dict_count/pw_count}')
        # print(dict_count/len(words))
        if dict_count > pw_count and pw_count != 0 and dict_count/len(words) > 0.5: #and  dict_count/pw_count > self.config.get_ratio():
            # print(pw_count, dict_count)
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