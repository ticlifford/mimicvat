#!/usr/bin/python3

import os 
import project_flask
import datetime
import time

print('running dailytask')
fPath = '/home/timc/flask_project/flask_app/daily.txt'
#fPath = 'daily.txt'

# get the date

ts = time.time()
dailyTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M')
print('test getTime:',dailyTime)

with open(fPath, 'a') as f:
#with open('daily.txt', 'a') as f:
    f.write("\n" 'edited on: ' + dailyTime)


# runs price scraper, then buylist scraper



# set price scraper

try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/setPriceScraper.py')
    with open(fPath, 'a') as f:
        f.write("\n" 'running set price scraper')
except:
    print('could not run setpricescraper')
    with open(fPath, 'a') as f:
        f.write("\n" 'setpricescraper didnt run')



# buylist scraper

try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/buylistsetscraper.py')
    with open(fPath, 'a') as f:
        f.write("\n" 'running buylistscraper')
except:
    with open(fPath, 'a') as f:
        f.write("\n" 'buylist scraper didnt run')

try:
    rows = project_flask.getWatchList()
    with open(fPath, 'a') as f:
        f.write("\n" 'running getWatchList')
except:
    print('could not access getwatchlist')
    with open(fPath, 'a') as f:
        f.write("\n" 'could not access getwatchlist')



# refreshes the watchlist trends

print("updating watchlist")
try:
    for row in rows:
        project_flask.updateTrend(row[1])
        print('updating',row[1])
    with open(fPath, 'a') as f:
        f.write("\n" 'processing watchlist updates')
except:
    print('could not access updateTrend')
    with open(fPath, 'a') as f:
        f.write("\n" 'could not access updateTrend')

with open(fPath, 'a') as f:
    f.write("\n" 'editing done: ' + dailyTime)
