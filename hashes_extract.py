with open("top1000000_polars", "r") as f:
    lines = f.readlines()
with open("password_list_hashes_3.txt", "w") as f:
    for line in lines:
        try:
            hashs = line.split(":")[0]
            f.write(hashs + '\n')
        except IndexError:
            print(line)
            breakpoint()