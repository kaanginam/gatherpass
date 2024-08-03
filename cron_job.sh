#!/bin/bash
cd /home/inam/gatherpass 
source .env/bin/activate 
python3 google_paste_scraper.py >> /home/inam/cronlog_pastes.log
