import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys

#'''
fPath = '/home/timc/flask_project/flask_app/daily.txt'
csvPath = '/home/timc/flask_project/flask_app/setNames.csv'
dbPath = '/home/timc/flask_project/flask_app/CARDINFO.db'
#'''

"""
fPath = 'C:/Users/tim/Documents/github_projects/mimicvat/daily.txt'
csvPath = 'C:/Users/tim/Documents/github_projects/mimicvat/setNames.csv'
dbPath = 'C:/Users/tim/Documents/github_projects/mimicvat/CARDINFO.db'
"""

with open(fPath, 'a') as f:
    f.write('\n set price scraper crontab:')


# scryfall breaks large sets up into multiple pages of cards, and 'has_more'/'next_page'
# are used to indicate this. checkPage lets me parse through the pages to run dailyPrice on each page of cards
def checkPage(data):
    try:
        print('checking page:')
        if data['has_more'] == True:
                print('I found another page of cards')
                jason_obj = urllib.request.urlopen(data['next_page'])
                data = json.load(jason_obj)
                dailyPrice(data)
    except:
        print('check page could not perform loop')

# set generation makes the URL for the api call with my set codes (like SOM for scars of mirrodin, etc) and runs the first daily price
# the checkPage function is recursive in dailyPrice
def setGeneration(set):

    try:
        print('the set is',set)
    except:
        with open(fPath, 'a') as f:
            f.write('\n could not print set in setgen')

    with open(fPath, 'a') as f:
        f.write('\n scraping:'+set)
    url = "https://api.scryfall.com/cards/search?q=set%3D" + set
    print('sleeping now')
    time.sleep(.600)
    print('the url is',url)
    try:
        jason_obj = urllib.request.urlopen(url)
        data = json.load(jason_obj)
        dailyPrice(data)
        with open(fPath, 'a') as f:
            f.write('\n correctly scraping set:'+set)
    except:
        print('something went wrong with set',set)
        with open(fPath, 'a') as f:
            f.write('\n problem scraping set:'+set)

def getTime():
    try:
            ts = time.time()
            dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            return dateTime
    except:
            print('getTime didnt work')
            with open(fPath, 'a') as f:
                f.write('\n couldnt run getTime')
print('test getTime:',getTime())

def foilRatio():
    try:
            foilRatio = float(obj['prices']['usd_foil'])/float(obj['prices']['usd'])
            return foilRatio
    except:
            return None

# the function that does most of the work. It gets passed a json with cards, and breaks up the card's info
# the card data is packed with all kinds of stuff like card id, name, price, color, text, images etc.
# I just use id and prices here.
def dailyPrice(data):
    for obj in data['data']:
        foilCalc = None
        usd = None
        foilUsd = None

        if obj['prices']['usd_foil'] == None:
                None
        else:
                foilUsd = obj['prices']['usd_foil']
        if obj['prices']['usd_foil'] == None or obj['prices']['usd']==None:
                foilCalc = None
        else:
                foilCalc = float(obj['prices']['usd_foil'])/float(obj['prices']['usd'])

        try:

            c.execute('insert into PRICES values (?,?,?,?,?)',(
            obj['id'],
            current_time,
            obj['prices']['usd'],
            obj['prices']['usd_foil'],
            foilCalc
            ))

            c.execute('insert or replace into PRICETODAY values (?,?,?)',(
            obj['id'],
            obj['prices']['usd'],
            obj['prices']['usd_foil']
            ))


        except:
                print('could not add to db')
                print( 'id:', obj['id'],'usd:' ,obj['prices']['usd'], 'foil:', obj['prices']['usd_foil'])
                sys.exit()
    try:
        checkPage(data)
    except:
        print('could not checkPage')

def printDb():
    try:
        print('im printing the db here:')
        for row in c.execute('SELECT * FROM PRICES'):
                print(row)
    except:
        print('could not print prices db')

try:
    print('setPricescraper connecting to db')
    with open(fPath, 'a') as f:
        f.write('\n setPricescraper connecting to db')
    cardsDb = sqlite3.connect(dbPath)
    c = cardsDb.cursor()
except:
    print('couldnt connect to db')
    with open(fPath, 'a') as f:
        f.write('\n setPricescraper could not connect to db')

try:
    c.execute('delete from PRICETODAY')
except:
    print('could not wipe prices today')

try:
    current_time = getTime()
except:
    print('could not get current time')

try:
    with open(csvPath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            print(line[0])
            setGeneration(line[0])

except:
    print('could not open csvPath')


cardsDb.commit()
print('im closing the db')
cardsDb.close()

with open(fPath, 'a') as f:
    f.write('\n finished running set price scraper')
