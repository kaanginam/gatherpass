import requests
import logging
import time
"""
Small snippet to deal with notifications for ntfy
"""
def notify(tpc, text):
    try:
        # Some texts have non ASCII characters so fix that
        requests.post(tpc, data=text.encode(encoding='utf-8'))
    except requests.exceptions.ConnectionError as e:
        # Due to some limitations of the frequency of posting, a small sleep helps out sometimes.
        logging.info('Too many notifications, waiting...')
        time.sleep(30)
        try:
            requests.post(tpc, data=text.encode(encoding='utf-8'))
        except requests.exceptions.ConnectionError as e:
            logging.error('Connection to ntfy.sh not possible')