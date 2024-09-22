#!/bin/bash
cd /home/inam/gatherpass 
source .env/bin/activate 
python google_paste_scraper.py >> /home/inam/cronlog_pastes.log