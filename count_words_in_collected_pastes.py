import re
import os
import hashlib
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import enchant
import datetime
import threading
from langdetect import detect
from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
#with open('password_list_hashes_3.txt', 'r') as f:
#    passhashs = f.read().splitlines()
def is_url(line):
    try:
        res = urlparse(line)
        return all([res.scheme, res.netloc])
    except AttributeError:
        return False
def is_email(word):
    if '@' in word:
        breakpoint()
    if re.match(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", word):
        return True
    return False
def get_words(text):
    seperators = [':', '|']
    lines = text.split("\n")
    pw_count = 0
    words = []
    i = 0
    for line in lines:
        if i == 0:
            i += 1
            continue
        if is_url(line):
            continue
        if line == '\n' or line == '':
            continue
        words.append(line)
        if " " in line:
            for s in line.split(" "):
                if s != '' and s != '\n':
                    words.append(s)
        for word in words:
            for sep in seperators:
                if sep in word: 
                    for s in word.split(sep):   
                        if s != '' and s != '\n':
                            words.append(s)
    return words
def has_credentials(words):
    for word in words:
        hexxed = hashlib.sha1(word.encode()).hexdigest()
        if hexxed.upper() in passhashs or hexxed in passhashs:
            return True
    return False
def count_passwords(words):
    counter = 0
    for word in words:
        hexxed = hashlib.sha1(word.encode()).hexdigest()
        if hexxed.upper() in passhashs or hexxed in passhashs:
            print(word)
            counter += 1
    return counter

def count_dictionary(words):
    d = enchant.Dict("en_US")
    counter = 0
    for word in words:
        if d.check(word):
            counter += 1
    return counter

def count_both(words, lang):
    counter = 0
    counter2 = 0
    d = enchant.Dict(lang)
    for word in words:
        hexxed = hashlib.sha1(word.encode()).hexdigest()
        if hexxed.upper() in passhashs or hexxed in passhashs:
            counter += 1
            print("is a pw", word)
        if d.check(word):
            counter2 += 1
            print("is a word", word)
    return counter, counter2
def count_from_file2(filename):
    real_fn = filename.split('/')[-1].strip()
    with open('pastes_counting2/output' + real_fn + '.txt', 'w') as f:
        f.write(f'Starting for file {filename} the counting\n')
    with open(filename, 'r', encoding='ISO-8859-1') as f:
        text = f.read()
    words = get_words(text)
    cnt, cnt2 = count_both(words)
    with open('pastes_counting2/output' + real_fn + '.txt', 'a') as f:
        f.write(f'{filename}: pws: {cnt} dict: {cnt2}\n')
    
def get_language(text):
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
def count_from_file(filename):
    real_fn = filename.split('/')[-1].strip()
    print(f'Starting for file {filename} the counting')
    with open(filename, 'r') as f:
        text = f.read()
    lang = get_language(text)
    
    print(lang)
    words = get_words(text)
    cnt, cnt2 = count_both(words, lang)
    print(f'{filename}: pws: {cnt} dict: {cnt2} ratio: {cnt/cnt2}')

numspw = 0
numslines = 0
ratios = 0

word_lens = 0
pws = 0
english = 0
thread_list = []
import sys
subdir = f"{sys.argv[1]}"
fns = os.listdir(subdir)
#for fn in fns:
#count_from_file(sys.argv[1])
config = PassConfig("./conf.json")

i = 0
for fn in fns:
    parser = LeakParser("password_list_hashes_3.txt", config)
    if fn == "6SK1B5fz8zBun5gSG1BxCY.txt" or fn == "paste2.org.43":
        continue
    if i == 100:
        break
    i += 1
    with open(f'{subdir}{fn}', 'r', encoding='ISO-8859-1') as f:
        text = f.read()
    print(f'Working on {fn}')
    if 'from pastebin.ai' in text or 'from pastebin.com' in text or 'from www.bitbin.it' in text or 'from p.ip.fi' in text:
        text = "\n".join(text.splitlines()[1:])
    rett = parser.has_credentials(text)
    #count_from_file(sys.argv[1])
#print(f'Avg: Words {word_lens} Pws {pws} English {cnt2}')