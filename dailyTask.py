#!/usr/bin/python3
"""
This is a process that runs every day to collect
card data. It is run with a cron task on an ubuntu server at 6AM.
It collects the data by running a series of scrapers, and saves
the values into my database file.
It also updates the daily watchlist trends.
"""
import os 
import project_flask
import datetime
import time

print('running dailytask')
fPath = '/home/timc/flask_project/flask_app/daily.txt'
# get the date

ts = time.time()
dailyTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M')
print('test getTime:',dailyTime)

with open(fPath, 'a') as f:
#with open('daily.txt', 'a') as f:
    f.write('\n edited on: ' + dailyTime)

# update the set name table
print("updating set name list")
try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/setNameCollector.py')
    with open(fPath, 'a') as f:
        f.write('\n updated set name list')
except:
    print('could not update set name list')
    with open(fPath, 'a') as f:
        f.write('\n could not update set name list')



# set price scraper

try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/setPriceScraper.py')
    with open(fPath, 'a') as f:
        f.write('\n running set price scraper')
except:
    print('could not run setpricescraper')
    with open(fPath, 'a') as f:
        f.write('\n setpricescraper didnt run')

# frontpage scraper
try:
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/frontpagedb.py')
    with open(fPath, 'a') as f:
        f.write('\n running frontpagedb')
except:
    print('could not run frontpagedb')
    with open(fPath, 'a') as f:
        f.write('\n frontpagedb didnt run')

# buylist scraper
try:
    with open(fPath, 'a') as f:
        f.write('\n running buylistscraper')
    os.system(r'python3 /home/timc/flask_project/flask_app/scrapers/buylistsetscraper.py')

except:
    with open(fPath, 'a') as f:
        f.write('\n buylist scraper didnt run')

# get the watchlist, return rows
try:
    with open(fPath, 'a') as f:
        f.write('\n running getWatchList')
    rows = project_flask.getWatchList()

except:
    print('could not access getwatchlist')
    with open(fPath, 'a') as f:
        f.write('\n could not access getwatchlist')

# refreshes the watchlist trends
print("updating watchlist")
try:
    with open(fPath, 'a') as f:
        f.write('\n processing watchlist updates')
    for row in rows:
        project_flask.updateTrend(row['id'])
        print('updating',row['id'])

except:
    print('could not access updateTrend')
    with open(fPath, 'a') as f:
        f.write('\n could not access updateTrend')

# update the reserve list table
print("updating reserve list")
try:
    os.system(r'python3 /home/timc/flask_project/flask_app/RlDailyInsert.py')
    with open(fPath, 'a') as f:
        f.write('\n updated reserve list')
except:
    print('could not update reserve list')
    with open(fPath, 'a') as f:
        f.write('\n could not update reserve list')

print("updating top rl table")
try:
    os.system(r'python3 /home/timc/flask_project/flask_app/topReserveUpdate.py')
    with open(fPath, 'a') as f:
        f.write('\n updated top rl table')
except:
    print('could not update top rl table')
    with open(fPath, 'a') as f:
        f.write('\n could not update top rl table')

with open(fPath, 'a') as f:
    f.write('\n editing done: ' + dailyTime)
