#!/usr/bin/python3
"""
This is a process that runs every week to collect
card set data. It is run with a cron task on an ubuntu server at 6AM on Monday.
It collects the data by running a craper that checks scryfall for new sets.
It updates a sql database and a csv file.
"""
import os 
import final_project_flask
import datetime
import time

print('running weeklytask')
fPath = '/home/timc/flask_project/flask_app/weekly.txt'
# get the date

ts = time.time()
dailyTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M')
print('test getTime:',dailyTime)

with open(fPath, 'a') as f:
#with open('weekly.txt', 'a') as f:
    f.write("\n" 'edited on: ' + dailyTime)


# set name scraper
try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/setNameCollector.py')
    with open(fPath, 'a') as f:
        f.write("\n" 'running set Name Collector')
except:
    print('could not run set Name Collector')
    with open(fPath, 'a') as f:
        f.write("\n" 'set Name Collector didnt run')

#check for new cards

try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/setCardScraper.py')
    with open(fPath, 'a') as f:
        f.write("\n" 'running set card scraper')
except:
    print('could not run set card scraper')
    with open(fPath, 'a') as f:
        f.write("\n" 'set card scraper didnt run')

with open(fPath, 'a') as f:
    f.write("\n" 'editing done: ' + dailyTime)