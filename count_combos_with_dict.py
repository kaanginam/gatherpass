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
import sys
from langdetect import detect
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
    for line in lines:
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
def is_password(word):
    with open('password_list_hashes_3.txt', 'r') as f:
        for line in f:
            if line.strip() == word:
                return True
def count_passwords(words):
    counter = 0
    hexxed_list = []
    for word in words:
        hexxed = hashlib.sha1(word.encode()).hexdigest()
        hexxed_list.append(hexxed.upper())
    with open('password_list_hashes_3.txt', 'r') as f:
        passhashs = f.read().splitlines()
    for hexx in hexxed:
        if hexx in passhashs:
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
    with open('/home/inam/gatherpass/password_list_hashes_3.txt', 'r') as f:
        passhashs = f.read().splitlines()
    for word in words:
        hexxed = hashlib.sha1(word.encode()).hexdigest()
        if hexxed.upper() in passhashs or hexxed in passhashs:
            counter += 1
        if d.check(word):
            counter2 += 1
        #print(word)
    return counter, counter2
def count_from_file2(filename):
    just_name = filename.split("/")[-1].strip()
    with open('combo_counting2/output' + just_name + '.txt', 'w') as f:
        f.write(f'Starting for file {filename} the counting')
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    lang = detect(text)
    words = get_words(text)
    cnt, cnt2 = count_both(words, lang)
    with open('combo_counting2/output' + just_name + '.txt', 'a') as f:
        f.write(f'{filename}: pws: {cnt} dict: {cnt2}')
def count_from_file(filename):
    just_name = filename.split("/")[-1].strip()
    print(f'Starting for file {filename} the counting')
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    lang = detect(text)
    words = get_words(text)
    cnt, cnt2 = count_both(words, lang)
    
    print(f'{filename}: pws: {cnt} dict: {cnt2}')
#os.chdir("combos")
numspw = 0
numslines = 0
ratios = 0
#fns = os.listdir("./")
word_lens = 0
pws = 0
english = 0
thread_list = []
##for fn in fns:
#    print(fn)
#    count_from_file(fn)
count_from_file(sys.argv[1])
#    t = threading.Thread(target=count_from_file, args=(fn,))
#    thread_list.append(t)
#for t in thread_list:
#    t.start()
#for t in thread_list:
#    t.join()
#print(f'Avg: Words {word_lens} Pws {pws} English {cnt2}')