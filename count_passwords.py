import os
passwords = open('password_list.txt', 'r').readlines()
os.chdir("100pastes")
numspw = 0
numslines = 0
fns = os.listdir("./")
for fn in fns:
    num_passw = 0
    with open(fn, 'r') as f:
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines == 0:
            print(f'This file is empty: {fn}')
            continue
    for line in lines:
        for password in passwords:
            if password in line:
                num_passw += 1

    print(f'The filename {fn} had a total of {num_lines} lines and {num_passw} passwords. Ratio: {num_passw/num_lines}')
    numspw += num_passw
    numslines += num_lines
print(f'Average: {numspw/len(fns)} passwords, {numslines/len(fns)} lines')
            