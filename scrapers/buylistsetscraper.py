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

# variables

cardNames = []
cardBuyPrices = []

# this function takes in a set and creates a url
# it scrapes the url into a soup
# it checks the list, evens and odds, for cards and prices
# it adds those values to lists when found


# get timestamp here and set as a var

# create a list in the format of [[cardname, cardset, buyprice, datestamp],[another card]] called sqlList

#gets the datetime
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
                #buyp = x.find('td', {'class' : 'buylistMarketPrice'}).get_text()
                #print('scraping')
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
        #foundSet = x.find('value')
        #print(foundSet)
        #print(x)
        #print(x.find_all('option'))
        for y in x.find_all('option'):

            # this gets the text of sets
            # print(y.get_text())

            # 
            print(y['value'])
            setLinks.append(y['value'])
    print('ending scrape')

def writeSets():
    with open ('setLinks.csv', 'w', newline='') as csv_file:
        cw = csv.writer(csv_file)
        for x in setLinks:
            cw.writerow([x])
        #cw.writerows([setLinks])

def addCards(setLinks):
    for cardSet in setLinks:
        print('sending set to addcards:',cardSet)
        scrape(cardSet)

def writeSql(cardName,dateTime,setName,buyPrice):
    try:
        # print(type(rarity))
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


# connect to db
cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()
dateTime = getTime()

# do something in db
#scrape("aer")
getSets()
fullScrape(setLinks)

cardsDb.commit()
print('im closing the db')
cardsDb.close()




#getSets()
#writeSets()

#addCards(setLinks)
