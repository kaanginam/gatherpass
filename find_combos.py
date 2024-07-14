import os
import re
passwords = open('password_list.txt', 'r').readlines()
os.chdir("100pastes")
numspw = 0
numslines = 0
fns = os.listdir("./")
new_pws = []
for fn in fns:
    num_passw = 0
    with open(fn, 'r') as f:
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines == 0:
            print(f'This file is empty: {fn}')
            continue
    """
    try:
        
        print(fn, lines[0], pw)
    except Exception as e:
        continue
    """ 
    for line in lines:
        splitted = line.strip().split(':')
        #if len(splitted) == 2:
            #print(fn, splitted[1])
        #splitted = line.strip().split(':')
        try:
            if len(splitted) < 2 or splitted[1] == '' or (splitted[1][0] == '/' and splitted[1][1] == '/'):
                #breakpoint()
                continue
        except IndexError as e:
            print(e)
            breakpoint()
        pw = splitted[1]
        if '|' in pw:
            pw = pw.split('|')[0]
        for password in passwords:
            if password == pw:
                num_passw += 1
        if num_passw == 0:
            new_pws.append(pw)
    print(f'The filename {fn} had a total of {num_lines} lines and {num_passw} passwords. Ratio: {num_passw/num_lines}')                
        
    # breakpoint()
print(f'Average: {numspw/len(fns)} passwords, {numslines/len(fns)} lines')
print("New passwords: ")
for npw in new_pws:
    print(npw)