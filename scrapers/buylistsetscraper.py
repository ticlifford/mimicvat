import urllib.request
from bs4 import BeautifulSoup as b
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys
from db_location import dbLoc

cardNames = []
cardBuyPrices = []

# this function takes in a set and creates a url
# it scrapes the url into a soup
# it checks the list, evens and odds, for cards and prices
# it adds those values to lists when found


# create a list in the format of [[cardname, cardset, buyprice, datestamp],[another card]] called sqlList

def getTime():
        try:
                ts = time.time()
                dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                return dateTime
        except:
                print('getTime didnt work')
print('test getTime:',getTime())

def scrape(setName):
    print('performing a scrape of set:', setName)
    url = "https://shop.tcgplayer.com/price-guide/magic/" + setName
    print('setting up soup')
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')
    try:
        #even
        for x in soup.find_all('tr', {'class' : 'even'}):
            cardName = x.find('div', {'class' : 'productDetail'}).get_text().rstrip().strip()
            buyPrice = x.find('td', {'class' : 'buylistMarketPrice'}).get_text().rstrip().strip()
            print('cardName:',cardName)
            print('buyprice:',buyPrice[1:])
            cardNames.append(cardName)
            try:
                writeSql(cardName,dateTime,setName,buyPrice)
            except:
                print('could not write sql')
            try:
                
                if buyPrice == u'\u2014':
                    cardBuyPrices.append(float(0))
                else:
                    cardBuyPrices.append(float(buyPrice[1:]))
            except:
                print('could not append prices')

        #odd
        for x in soup.find_all('tr', {'class' : 'odd'}):
            cardName = x.find('div', {'class' : 'productDetail'}).get_text().rstrip().strip()
            buyPrice = x.find('td', {'class' : 'buylistMarketPrice'}).get_text().rstrip().strip()
            print('cardname:',cardName)
            print('buyprice:',buyPrice[1:])
            cardNames.append(cardName)
            try:
                writeSql(cardName,dateTime,setName,buyPrice)
            except:
                print('could not write sql')
            try:
                if buyPrice == u'\u2014':
                    cardBuyPrices.append(float(0))
                else:
                    cardBuyPrices.append(float(buyPrice[1:]))
            except:
                print('could not append prices')
    except:
        print('something went wrong with scrape URL')
    print('lists:')
    print(cardBuyPrices)

setLinks = []

def getSets():

    url = "https://shop.tcgplayer.com/price-guide/magic/"

    # set up soup
    html = urllib.request.urlopen(url).read()
    soup = b(html, 'html.parser')


    print('starting scrape')
    for x in soup.find_all('select', {'class' : 'priceGuideDropDown', 'id' : 'set'}):
        for y in x.find_all('option'):
            print(y['value'])
            setLinks.append(y['value'])
    print('ending scrape')

def writeSets():
    with open ('setLinks.csv', 'w', newline='') as csv_file:
        cw = csv.writer(csv_file)
        for x in setLinks:
            cw.writerow([x])

def addCards(setLinks):
    for cardSet in setLinks:
        print('sending set to addcards:',cardSet)
        scrape(cardSet)

def writeSql(cardName,dateTime,setName,buyPrice):
    try:
        c.execute('insert or ignore into BUYLIST values (?,?,?,?)',(
        cardName,
        dateTime,
        setName,
        buyPrice[1:]
        ))
    except:
        print('could not write sql function')

def fullScrape(setLinks):
    for cardSet in setLinks:
        scrape(cardSet)

cardsDb = sqlite3.connect(dbLoc)
c = cardsDb.cursor()
dateTime = getTime()
getSets()
fullScrape(setLinks)
cardsDb.commit()
print('im closing the db')
cardsDb.close()
