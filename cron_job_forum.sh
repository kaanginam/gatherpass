#!/bin/bash
cd /home/inam/gatherpass 
source .env/bin/activate 
# python google_paste_scraper.py >> /home/inam/cronlog_pastes.log
python forum_scraper.py >> /home/raspi/cronlog_threads.log