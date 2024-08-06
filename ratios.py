import os
fns = os.listdir('pastes_counting/')
for fn in fns:
    with open(f'pastes_counting/{fn}', 'r') as f:
        content = f.read()
    splitted = content.strip().split(":")
    try:
        pws = splitted[-2].split(" ")[1]
    except IndexError as e:
        continue
    print(f"FN: {fn}, PWS: {pws}, Words: {splitted[-1]}")