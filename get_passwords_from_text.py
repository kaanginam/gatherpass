from passscrape.leakparser import LeakParser
from passscrape.passconfig import PassConfig
from passscrape.googlescraper import GoogleScraper
import logging, sys
text = """
justpaste.me
https://mxcd.online/login - EMAIL : jimmynguyen3.1415@gmail.com - PASSWORD : ASNguyen12
https://mxcd.online/login - EMAIL : dwight.johnson@gmail.com - PASSWORD : 1997johns4
"""
lines = open('100pastes/paste2.org.28').readlines()
text2 = "\n".join(lines[1:])
config = PassConfig('./conf.json')
parser = LeakParser(
    config.get_passlist(), 
    config.get_seperators(),
    config.get_ignore_list(),
    config.get_ratio(),
    config.get_any_pw()
)
if config.get_debug():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
output, words = parser.has_credentials(text2)
# jwords = []
dwords = []
pwords = []
for word in words:
    # jwords.append(word["txt"])
    # print(word["txt"])
    if word["is_dict"]: #and not word["is_pw"]:
        # print("is dict:", word["txt"])
        dwords.append(word["txt"])
    if word["is_pw"]:
        pwords.append(word["txt"])
    #if word["is_pw"]:
    #    print("is pw", word["txt"])
    
print(dwords)
print(pwords)
print(output)