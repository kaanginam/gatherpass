import requests
import logging
import time
"""
Small snippet to deal with notifications for ntfy
"""
def notify(tpc, text):
    try:
        requests.post(tpc, data=text.encode(encoding='utf-8'))
    except requests.exceptions.ConnectionError as e:
        logging.info('Too many notifications, waiting...')
        time.sleep(10)
        try:
            requests.post(tpc, data=text.encode(encoding='utf-8'))
        except requests.exceptions.ConnectionError as e:
            logging.error('Connection to ntfy.sh not possible')