#!/bin/bash
cd /home/inam/gatherpass 
source .env/bin/activate 
python forum_scraper.py >> /home/raspi/cronlog_threads.log