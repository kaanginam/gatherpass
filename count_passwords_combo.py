import os
import hashlib
import requests
import time
#passwords = open(r'/mnt/c/Users/Kaneki Ken/pwnedpasswords_all_2.txt', 'r').readlines()
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
        if hexxed.upper() == (hexxed[0:5].upper()+h.strip().split(":")[0]):
            return True
    return False
os.chdir("combos")
numspw = 0
numslines = 0
ratios = 0
fns = os.listdir("./")
#print(fns)
with open('../password_list_hashes_3.txt', 'r') as f:
    passhashs = f.read().splitlines()
for fn in fns:
    num_passw = 0
    mail_count = 0
    print(fn)
    with open(fn, 'r', encoding="utf8") as f:
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines == 0:
            print(f'This file is empty: {fn}')
            continue
    for line in lines:
        if line == '\n':
            continue
        try:
            if "|" in line:
                pw_in_line = line.split('|')[0].split(":")[1].strip()
            elif ":" in line:
                if "http://" in line or "https://" in line:
                    continue
                pw_in_line = line.split(":")[1].strip()
        except IndexError:
            continue
        if "@" in line:
            mail_count += 1
        try:
            hexxed = hashlib.sha1(pw_in_line.encode()).hexdigest()
        except UnicodeDecodeError as e:
            print(e)
            breakpoint()
        if hexxed.upper() in passhashs:
            num_passw += 1
        #if password_in_hibp(pw_in_line):
        #    num_passw += 1
        #time.sleep(3)
    ratios += num_passw/num_lines
    print(f'The filename {fn} had a total of {num_lines} lines and {num_passw} passwords. Ratio: {num_passw/num_lines}. Mails: {mail_count}')
    numspw += num_passw
    numslines += num_lines
    
print(f'Average: {numspw/len(fns)} passwords, {numslines/len(fns)} lines, {ratios/len(fns)} ratio')
            