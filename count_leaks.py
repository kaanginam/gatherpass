user_list = []
filename = 'T_leaks_gathered'
lines = open(filename, 'r').readlines()
for line in lines:
    combo = line
    if "\n" == line:
        continue
    if " " in line:
        splitted = line.split(" ")
        for spl in splitted:
            if ":" in spl:    
                combo = spl
                break
    splcombo = combo.split(":")
    
    found = False
    # print(combo)
    for user in user_list:
        if user["user"] == splcombo[0] and splcombo[1] == user["pw"]:
            found = True
            print("found", user, splcombo)
    if not found:
        user_list.append({
                "user": splcombo[0].strip(),
                "pw": splcombo[1].strip()
                })
print(len(user_list))