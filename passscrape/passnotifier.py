import requests
def notify(tpc, text):
    requests.post(tpc, 
    data=text.encode(encoding='utf-8'))
